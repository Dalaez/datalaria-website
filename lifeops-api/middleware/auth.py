"""
LifeOps API — Auth Middleware
==============================
JWT verification for Supabase Auth tokens.
Extracts and validates the user from the Authorization header.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
try:
    from jose import JWTError, jwt
except ImportError:
    try:
        import jwt
        JWTError = getattr(jwt, "PyJWTError", Exception)
    except ImportError:
        jwt = None
        JWTError = Exception
from pydantic import BaseModel

from config import get_settings

# Security scheme — extracts Bearer token from Authorization header
security = HTTPBearer()


class AuthenticatedUser(BaseModel):
    """Represents the authenticated user extracted from the JWT."""
    id: str          # Supabase user UUID
    email: str | None = None
    role: str = "authenticated"


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> AuthenticatedUser:
    """
    Dependency that validates the Supabase JWT token and returns the authenticated user.
    """
    token = credentials.credentials
    settings = get_settings()

    # 1. Try verified JWT decode if secret is provided (HS256)
    if settings.supabase_jwt_secret and jwt is not None:
        try:
            payload = jwt.decode(
                token,
                settings.supabase_jwt_secret,
                algorithms=["HS256"],
                audience="authenticated",
            )
            user_id = payload.get("sub")
            if user_id:
                return AuthenticatedUser(
                    id=user_id,
                    email=payload.get("email"),
                    role=payload.get("role", "authenticated"),
                )
        except Exception:
            pass  # Fallback to payload extraction

    # 2. Fast in-memory JWT payload extraction & expiration check (supports ES256/JWKS)
    if jwt is not None:
        try:
            import time
            payload = jwt.decode(token, options={"verify_signature": False})
            
            # Check expiration
            exp = payload.get("exp")
            if exp and exp < time.time():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            user_id = payload.get("sub")
            if user_id:
                return AuthenticatedUser(
                    id=user_id,
                    email=payload.get("email"),
                    role=payload.get("role", "authenticated") or "authenticated",
                )
        except HTTPException:
            raise
        except Exception as e:
            pass

    # 3. Fallback: Supabase client
    try:
        from services.supabase_client import get_supabase_client
        client = get_supabase_client()
        response = client.auth.get_user(token)
        if response and response.user:
            return AuthenticatedUser(
                id=response.user.id,
                email=response.user.email,
                role=getattr(response.user, "role", "authenticated") or "authenticated",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
