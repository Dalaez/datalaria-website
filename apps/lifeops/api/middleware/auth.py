"""
LifeOps API — Auth Middleware
==============================
Cryptographic JWT verification for Supabase Auth tokens.
Supports local zero-network verification for both asymmetric ECC P-256 (ES256/RS256)
via cached JWKS and legacy symmetric HS256 via SUPABASE_JWT_SECRET.
Enforces SEC-1 and INV-17 (never accepts unverified tokens; never falls back to network
on forged or expired signatures).
"""
from functools import lru_cache
import logging
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

import jwt
from jwt import PyJWKClient
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidIssuerError,
    InvalidSignatureError,
    InvalidTokenError,
    PyJWKClientConnectionError,
    PyJWKClientError,
)

from config import get_settings

logger = logging.getLogger(__name__)

# Security scheme — extracts Bearer token from Authorization header
security = HTTPBearer(auto_error=True)

_ASYMMETRIC_ALGS = ("ES256", "RS256")
_SUPPORTED_ALGS = ("HS256",) + _ASYMMETRIC_ALGS


class AuthenticatedUser(BaseModel):
    """Represents the authenticated user extracted from the verified JWT."""
    id: str          # Supabase user UUID
    email: Optional[str] = None
    role: str = "authenticated"


@lru_cache(maxsize=4)
def _get_jwks_client(supabase_url: str) -> PyJWKClient:
    """Return cached PyJWKClient for Supabase Auth JWKS (1h TTL, 5s timeout)."""
    jwks_uri = f"{supabase_url.rstrip('/')}/auth/v1/.well-known/jwks.json"
    return PyJWKClient(
        jwks_uri,
        cache_keys=True,
        cache_jwk_set=True,
        lifespan=3600,
        timeout=5,
    )


def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def _user_from_payload(payload: dict) -> AuthenticatedUser:
    user_id = payload.get("sub")
    if not user_id:
        raise _unauthorized("Invalid token: missing subject (sub)")
    return AuthenticatedUser(
        id=str(user_id),
        email=payload.get("email"),
        role=payload.get("role", "authenticated") or "authenticated",
    )


def _verify_via_supabase_fallback(token: str, reason: str) -> AuthenticatedUser:
    """
    Network fallback to Supabase Auth API.
    ONLY invoked when local verification material is transiently unreachable (e.g. JWKS
    connection error or unconfigured legacy HS256 secret), NEVER after InvalidSignatureError.
    """
    logger.warning("Local JWT verification unavailable (%s); falling back to Supabase Auth API", reason)
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
    except Exception as exc:
        logger.warning("Supabase Auth API validation failed: %s", exc)
        raise _unauthorized("Invalid authentication token")

    raise _unauthorized("Could not validate credentials")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> AuthenticatedUser:
    """
    Dependency that cryptographically validates the Supabase JWT token locally
    according to its header `alg` and returns the authenticated user (SEC-1 / INV-17).
    """
    token = credentials.credentials
    settings = get_settings()

    # 1. Inspect header algorithm safely (reject malformed tokens & alg=none immediately)
    try:
        header = jwt.get_unverified_header(token)
        alg = str(header.get("alg") or "").upper()
    except InvalidTokenError:
        raise _unauthorized("Malformed authentication token")

    if alg not in _SUPPORTED_ALGS:
        raise _unauthorized(f"Unsupported authentication algorithm: {alg or 'none'}")

    # 2. Symmetric HS256 (Legacy Supabase JWT Secret)
    if alg == "HS256":
        if not settings.supabase_jwt_secret:
            return _verify_via_supabase_fallback(token, "HS256 token without SUPABASE_JWT_SECRET configured")
        try:
            payload = jwt.decode(
                token,
                settings.supabase_jwt_secret,
                algorithms=["HS256"],
                audience="authenticated",
            )
            return _user_from_payload(payload)
        except ExpiredSignatureError:
            raise _unauthorized("Token has expired")
        except InvalidTokenError:
            # SEC-1 / INV-17: Forged or invalid HS256 signature -> immediate 401 (0 network calls)
            raise _unauthorized("Invalid authentication token")

    # 3. Asymmetric ECC P-256 (ES256) / RS256 via cached Supabase JWKS
    try:
        jwks_client = _get_jwks_client(settings.supabase_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=[alg],
            audience="authenticated",
        )
        return _user_from_payload(payload)
    except ExpiredSignatureError:
        raise _unauthorized("Token has expired")
    except (InvalidSignatureError, InvalidAudienceError, InvalidIssuerError, InvalidAlgorithmError):
        # SEC-1 / INV-17: Forged asymmetric signature -> immediate 401 (0 network calls)
        raise _unauthorized("Invalid authentication token")
    except PyJWKClientConnectionError as exc:
        # Transient network issue reaching Supabase JWKS endpoint -> controlled fallback
        return _verify_via_supabase_fallback(token, f"JWKS connection error: {exc}")
    except (PyJWKClientError, InvalidTokenError):
        # Unknown kid or invalid token structure -> reject immediately
        raise _unauthorized("Invalid authentication token")
