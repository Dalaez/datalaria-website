"""
LifeOps API — Authentication & Security Tests (SEC-1 & Invariants)
===================================================================
Tests cryptographic JWT verification to guarantee:
1. INV-1 & INV-2: Unauthenticated or expired tokens return 401.
2. SEC-1: Forged tokens signed with a different key are REJECTED (401),
   even if they contain an arbitrary user sub UUID.
3. Legitimate tokens signed with the configured secret are accepted.
"""
import time
import jwt
import pytest
from fastapi.testclient import TestClient
from main import app
from config import get_settings

client = TestClient(app)

SECRET = "test-secret-key-32-chars-long-minimum!!"


@pytest.fixture(autouse=True)
def configure_test_secret(monkeypatch):
    """Ensure the JWT secret is set for authentication tests."""
    monkeypatch.setattr(get_settings(), "supabase_jwt_secret", SECRET)


def test_auth_missing_header():
    """Unauthenticated request to protected endpoint should be rejected."""
    response = client.get("/api/v1/projects/")
    assert response.status_code in (401, 403)


def test_auth_expired_token():
    """Expired token must return 401."""
    expired_payload = {
        "sub": "user-12345",
        "email": "test@datalaria.com",
        "role": "authenticated",
        "aud": "authenticated",
        "exp": int(time.time()) - 3600,  # 1 hour in the past
    }
    token = jwt.encode(expired_payload, SECRET, algorithm="HS256")
    response = client.get("/api/v1/projects/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert "expired" in response.json().get("detail", "").lower()


def test_auth_forged_signature_rejection():
    """
    SEC-1 Security Fix:
    A token with an attacker payload signed with an attacker key MUST BE REJECTED.
    Under the old code (verify_signature: False), this would have bypassed auth!
    """
    attacker_secret = "attacker-unauthorized-fake-key!!"
    forged_payload = {
        "sub": "victim-user-uuid-99999",
        "email": "victim@datalaria.com",
        "role": "authenticated",
        "aud": "authenticated",
        "exp": int(time.time()) + 3600,
    }
    forged_token = jwt.encode(forged_payload, attacker_secret, algorithm="HS256")
    response = client.get("/api/v1/projects/", headers={"Authorization": f"Bearer {forged_token}"})
    assert response.status_code == 401


def test_auth_valid_token_acceptance(monkeypatch):
    """
    Valid token signed with real secret is decoded properly and accepts the user.
    """
    valid_payload = {
        "sub": "valid-user-11111",
        "email": "user@datalaria.com",
        "role": "authenticated",
        "aud": "authenticated",
        "exp": int(time.time()) + 3600,
    }
    valid_token = jwt.encode(valid_payload, SECRET, algorithm="HS256")

    # Mock the database call in projects router to avoid requiring real Supabase
    def mock_db(table_name):
        class MockQuery:
            def select(self, *args):
                return self
            def eq(self, *args):
                return self
            def order(self, *args, **kwargs):
                return self
            def limit(self, *args, **kwargs):
                return self
            def execute(self):
                class MockRes:
                    data = []
                return MockRes()
        return MockQuery()

    import routers.projects as r_projects
    monkeypatch.setattr(r_projects, "db", mock_db)

    response = client.get("/api/v1/projects/", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200
    assert response.json() == []


def test_activities_details_with_date_filters(monkeypatch):
    """
    INV-9 & INV-15: GET /api/v1/activities/details supports date_from, date_to
    and joins child records via PostgREST embedded select without .in_().
    """
    valid_payload = {
        "sub": "valid-user-11111",
        "email": "user@datalaria.com",
        "role": "authenticated",
        "aud": "authenticated",
        "exp": int(time.time()) + 3600,
    }
    valid_token = jwt.encode(valid_payload, SECRET, algorithm="HS256")

    recorded_filters = []
    recorded_selects = []

    def mock_db(table_name):
        class MockQuery:
            def __init__(self, tbl):
                self.tbl = tbl
            def select(self, clause, **kwargs):
                recorded_selects.append((self.tbl, clause))
                return self
            def eq(self, col, val):
                recorded_filters.append(("eq", self.tbl, col, val))
                return self
            def gte(self, col, val):
                recorded_filters.append(("gte", self.tbl, col, val))
                return self
            def lte(self, col, val):
                recorded_filters.append(("lte", self.tbl, col, val))
                return self
            def in_(self, col, vals):
                raise AssertionError("INV-15 violation: .in_() must not be called in /details")
            def order(self, *args, **kwargs):
                return self
            def limit(self, *args, **kwargs):
                return self
            def execute(self):
                class MockRes:
                    if self.tbl == "activities":
                        data = [
                            {
                                "id": "act-1",
                                "user_id": "valid-user-11111",
                                "activity_type": "sport",
                                "title": "10K Run",
                                "date": "2026-10-20",
                                "duration_minutes": 48,
                                "workouts": [
                                    {
                                        "id": "w-1",
                                        "activity_id": "act-1",
                                        "workout_type": "running",
                                        "distance_km": 10.0,
                                        "calories": 650,
                                    }
                                ],
                            }
                        ]
                    else:
                        data = []
                return MockRes()
        return MockQuery(table_name)

    import routers.activities as r_activities
    monkeypatch.setattr(r_activities, "db", mock_db)

    response = client.get(
        "/api/v1/activities/details?date_from=2026-10-01&date_to=2026-10-31&limit=500",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert "workouts" not in body[0]
    assert body[0]["workout"]["workout_type"] == "running"
    assert body[0]["workout"]["distance_km"] == 10.0
    assert ("eq", "activities", "user_id", "valid-user-11111") in recorded_filters
    assert ("gte", "activities", "date", "2026-10-01") in recorded_filters
    assert ("lte", "activities", "date", "2026-10-31") in recorded_filters
    assert any("workouts(*)" in clause for _, clause in recorded_selects)


# ── INV-17: Local ECC (P-256 / ES256) JWKS & Zero-Fallback on Forged Tokens ──

def _generate_ec_keypair():
    from cryptography.hazmat.primitives.asymmetric import ec
    private_key = ec.generate_private_key(ec.SECP256R1())
    return private_key, private_key.public_key()


def test_auth_forged_hs256_never_calls_supabase_fallback(monkeypatch):
    """INV-17: Forged HS256 token rejects with 401 immediately without network fallback."""
    import middleware.auth as auth_mod

    fallback_called = False

    def fail_if_called(*args, **kwargs):
        nonlocal fallback_called
        fallback_called = True
        raise AssertionError("Fallback must NOT be invoked on forged HS256 token")

    monkeypatch.setattr(auth_mod, "_verify_via_supabase_fallback", fail_if_called)

    forged = jwt.encode(
        {"sub": "victim-1", "aud": "authenticated", "exp": int(time.time()) + 3600},
        "wrong-secret-key-32-chars-minimum!!",
        algorithm="HS256",
    )
    response = client.get("/api/v1/projects/", headers={"Authorization": f"Bearer {forged}"})
    assert response.status_code == 401
    assert fallback_called is False


def test_auth_es256_jwks_valid_token_acceptance(monkeypatch):
    """INV-17: Valid ECC (P-256 / ES256) token is verified locally via cached JWKS with 0 network fallback."""
    import middleware.auth as auth_mod
    import routers.projects as r_projects

    priv_key, pub_key = _generate_ec_keypair()

    class MockSigningKey:
        key = pub_key

    class MockJWKSClient:
        def get_signing_key_from_jwt(self, token):
            return MockSigningKey()

    monkeypatch.setattr(auth_mod, "_get_jwks_client", lambda _url: MockJWKSClient())
    monkeypatch.setattr(
        auth_mod,
        "_verify_via_supabase_fallback",
        lambda *a, **kw: (_ for _ in ()).throw(AssertionError("Fallback must not be called")),
    )

    def mock_db(_tbl):
        class MockQ:
            def select(self, *a, **kw): return self
            def eq(self, *a, **kw): return self
            def order(self, *a, **kw): return self
            def limit(self, *a, **kw): return self
            def execute(self):
                class R:
                    data = []
                return R()
        return MockQ()

    monkeypatch.setattr(r_projects, "db", mock_db)

    es256_token = jwt.encode(
        {
            "sub": "ecc-user-uuid-1234",
            "email": "ecc@datalaria.com",
            "role": "authenticated",
            "aud": "authenticated",
            "exp": int(time.time()) + 3600,
        },
        priv_key,
        algorithm="ES256",
        headers={"kid": "b4563d07-a2aa-4ef9-95fc-0efe81647c83"},
    )

    response = client.get("/api/v1/projects/", headers={"Authorization": f"Bearer {es256_token}"})
    assert response.status_code == 200
    assert response.json() == []


def test_auth_es256_forged_signature_rejects_without_fallback(monkeypatch):
    """INV-17 / SEC-1: Forged ES256 token rejects with 401 immediately and never calls Supabase Auth."""
    import middleware.auth as auth_mod

    _legit_priv, legit_pub = _generate_ec_keypair()
    attacker_priv, _attacker_pub = _generate_ec_keypair()

    class MockSigningKey:
        key = legit_pub

    class MockJWKSClient:
        def get_signing_key_from_jwt(self, token):
            return MockSigningKey()

    monkeypatch.setattr(auth_mod, "_get_jwks_client", lambda _url: MockJWKSClient())
    monkeypatch.setattr(
        auth_mod,
        "_verify_via_supabase_fallback",
        lambda *a, **kw: (_ for _ in ()).throw(AssertionError("Fallback must NOT run on forged ES256")),
    )

    forged_es256 = jwt.encode(
        {"sub": "victim-uuid", "aud": "authenticated", "exp": int(time.time()) + 3600},
        attacker_priv,
        algorithm="ES256",
        headers={"kid": "b4563d07-a2aa-4ef9-95fc-0efe81647c83"},
    )
    response = client.get("/api/v1/projects/", headers={"Authorization": f"Bearer {forged_es256}"})
    assert response.status_code == 401


def test_auth_es256_expired_token_rejects_without_fallback(monkeypatch):
    """INV-17 / INV-2: Expired ES256 token returns 401 without network fallback."""
    import middleware.auth as auth_mod

    priv_key, pub_key = _generate_ec_keypair()

    class MockSigningKey:
        key = pub_key

    class MockJWKSClient:
        def get_signing_key_from_jwt(self, token):
            return MockSigningKey()

    monkeypatch.setattr(auth_mod, "_get_jwks_client", lambda _url: MockJWKSClient())
    monkeypatch.setattr(
        auth_mod,
        "_verify_via_supabase_fallback",
        lambda *a, **kw: (_ for _ in ()).throw(AssertionError("Fallback must NOT run on expired ES256")),
    )

    expired_es256 = jwt.encode(
        {"sub": "ecc-user", "aud": "authenticated", "exp": int(time.time()) - 120},
        priv_key,
        algorithm="ES256",
    )
    response = client.get("/api/v1/projects/", headers={"Authorization": f"Bearer {expired_es256}"})
    assert response.status_code == 401
    assert "expired" in response.json().get("detail", "").lower()


def test_auth_alg_none_rejected():
    """SEC-1 / INV-17: Unsigned alg=none token must be rejected immediately."""
    import base64, json

    hdr = base64.urlsafe_b64encode(json.dumps({"alg": "none", "typ": "JWT"}).encode()).rstrip(b"=").decode()
    pld = base64.urlsafe_b64encode(json.dumps({"sub": "admin", "aud": "authenticated"}).encode()).rstrip(b"=").decode()
    unsigned_token = f"{hdr}.{pld}."

    response = client.get("/api/v1/projects/", headers={"Authorization": f"Bearer {unsigned_token}"})
    assert response.status_code == 401


def test_auth_es256_jwks_connection_error_uses_fallback_with_warning(monkeypatch, caplog):
    """INV-17: Transient PyJWKClientConnectionError logs WARNING and falls back to Supabase Auth API."""
    import logging
    from jwt.exceptions import PyJWKClientConnectionError
    import middleware.auth as auth_mod
    import routers.projects as r_projects

    priv_key, _ = _generate_ec_keypair()

    class FailingJWKSClient:
        def get_signing_key_from_jwt(self, token):
            raise PyJWKClientConnectionError("Temporary DNS glitch")

    class FakeUser:
        id = "fallback-user-999"
        email = "fallback@datalaria.com"
        role = "authenticated"

    class FakeAuthRes:
        user = FakeUser()

    class FakeSupabaseAuth:
        def get_user(self, token):
            return FakeAuthRes()

    class FakeSupabaseClient:
        auth = FakeSupabaseAuth()

    monkeypatch.setattr(auth_mod, "_get_jwks_client", lambda _url: FailingJWKSClient())
    import services.supabase_client as sb_mod
    monkeypatch.setattr(sb_mod, "get_supabase_client", lambda: FakeSupabaseClient())

    def mock_db(_tbl):
        class MockQ:
            def select(self, *a, **kw): return self
            def eq(self, *a, **kw): return self
            def order(self, *a, **kw): return self
            def limit(self, *a, **kw): return self
            def execute(self):
                class R:
                    data = []
                return R()
        return MockQ()

    monkeypatch.setattr(r_projects, "db", mock_db)

    es256_token = jwt.encode(
        {"sub": "fallback-user-999", "aud": "authenticated", "exp": int(time.time()) + 3600},
        priv_key,
        algorithm="ES256",
    )

    with caplog.at_level(logging.WARNING, logger="middleware.auth"):
        response = client.get("/api/v1/projects/", headers={"Authorization": f"Bearer {es256_token}"})

    assert response.status_code == 200
    assert any("falling back to Supabase Auth API" in rec.message for rec in caplog.records)
