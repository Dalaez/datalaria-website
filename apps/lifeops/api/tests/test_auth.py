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
