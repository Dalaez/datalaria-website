"""
LifeOps API — Auth Middleware
==============================
Cryptographic JWT verification for Supabase Auth tokens.
Extracts and validates the user from the Authorization header.
Enforces SEC-1 (strict signature verification).
"""
import logging
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from config import get_settings

logger = logging.getLogger(__name__)

# Security scheme — extracts Bearer token from Authorization header
security = HTTPBearer(auto_error=True)


class AuthenticatedUser(BaseModel):
    """Represents the authenticated user extracted from the verified JWT."""
    id: str          # Supabase user UUID
    email: Optional[str] = None
    role: str = "authenticated"


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> AuthenticatedUser:
    """
    Dependency that cryptographically validates the Supabase JWT token
    and returns the authenticated user.
    Never accepts unverified tokens (SEC-1 fix).
    """
    token = credentials.credentials
    settings = get_settings()

    # 1. Try verified JWT decode via shared secret (HS256) if configured
    if settings.supabase_jwt_secret:
        try:
            payload = jwt.decode(
                token,
                settings.supabase_jwt_secret,
                algorithms=["HS256"],
                audience="authenticated",
            )
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing subject (sub)",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return AuthenticatedUser(
                id=user_id,
                email=payload.get("email"),
                role=payload.get("role", "authenticated") or "authenticated",
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except InvalidTokenError as e:
            logger.debug("Local HS256 JWT verification failed: %s", e)

    # 2. Cryptographic verification via Supabase Auth API (supports ES256/RS256/JWKS)
    try:
        from services.supabase_client import get_supabase_client
        client = get_supabase_client()
        response = client.auth.get_user(token)
        if response and response.user and response.user.id:
            return AuthenticatedUser(
                id=str(response.user.id),
                email=response.user.email,
                role=getattr(response.user, "role", "authenticated") or "authenticated",
            )
    except Exception as e:
        logger.warning("Supabase auth validation failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
