"""
LifeOps API — Auth Middleware
==============================
JWT verification for Supabase Auth tokens.
Extracts and validates the user from the Authorization header.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from config import get_settings

# Security scheme — extracts Bearer token from Authorization header
security = HTTPBearer()


class AuthenticatedUser(BaseModel):
    """Represents the authenticated user extracted from the JWT."""
    id: str          # Supabase user UUID
    email: str | None = None
    role: str = "authenticated"


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> AuthenticatedUser:
    """
    Dependency that validates the Supabase JWT token and returns the authenticated user.
    """
    token = credentials.credentials
    settings = get_settings()

    # 1. Try local JWT decode if secret is provided
    if settings.supabase_jwt_secret:
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
        except JWTError:
            pass  # Fallback to Supabase Auth API

    # 2. Verify token via Supabase Auth SDK (supports JWKS and new API Key system)
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
        detail="Invalid authentication token or user not found",
        headers={"WWW-Authenticate": "Bearer"},
    )
