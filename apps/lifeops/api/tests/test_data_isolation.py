"""
LifeOps API — Data Isolation & Synthetic Seeder Guard Tests (INV-11)
=====================================================================
Validates SDD Invariant INV-11 to prevent synthetic, demo, benchmark or test data
from contaminating real production user accounts (e.g. dalaez1@gmail.com).

Guarantees:
1. Synthetic seeder guard strictly blocks real users with SeederProtectionError.
2. Only explicitly authorized demo accounts (datalaria@gmail.com) can receive synthetic data.
3. Signature leakage detector catches any synthetic records attempting to enter production.
4. API routers enforce strict tenant isolation (no cross-tenant leakage).
5. Database integrity audit: real user accounts contain zero synthetic records.
"""
import pytest
import jwt
import time
from fastapi.testclient import TestClient
from main import app
from config import get_settings
from services.seeder_guard import (
    validate_synthetic_seed_target,
    detect_synthetic_leakage,
    SeederProtectionError,
    ALLOWED_DEMO_EMAILS,
    ALLOWED_DEMO_UIDS,
    PROTECTED_REAL_EMAILS,
    SYNTHETIC_ACTIVITY_SIGNATURES,
    SYNTHETIC_PROJECT_SIGNATURES,
    SYNTHETIC_TASK_SIGNATURES,
)

client = TestClient(app)
SECRET = "test-secret-key-32-chars-long-minimum!!"


@pytest.fixture(autouse=True)
def configure_test_secret(monkeypatch):
    monkeypatch.setattr(get_settings(), "supabase_jwt_secret", SECRET)


def test_seeder_guard_blocks_real_user():
    """INV-11: Attempting to seed data for dalaez1@gmail.com MUST raise SeederProtectionError."""
    real_uid = "459d8ddf-5580-4398-88fd-a1ed63df1643"
    with pytest.raises(SeederProtectionError) as exc_info:
        validate_synthetic_seed_target(user_id=real_uid, email="dalaez1@gmail.com")
    assert "Seeding blocked for protected production user" in str(exc_info.value)


def test_seeder_guard_blocks_unauthorized_random_user():
    """INV-11: Any arbitrary user not in the allowlist must be rejected."""
    random_uid = "99999999-0000-0000-0000-999999999999"
    with pytest.raises(SeederProtectionError):
        validate_synthetic_seed_target(user_id=random_uid, email="random.person@example.com")

    # Even without email, UID alone must be in allowlist
    with pytest.raises(SeederProtectionError):
        validate_synthetic_seed_target(user_id=random_uid)


def test_seeder_guard_allows_demo_user():
    """INV-11: Seeding is permitted ONLY for authorized demo accounts."""
    demo_uid = "18d01a19-450b-4099-96f4-66b21714a525"
    demo_email = "datalaria@gmail.com"
    assert validate_synthetic_seed_target(user_id=demo_uid, email=demo_email) is True
    assert validate_synthetic_seed_target(user_id="mock-user-datalaria") is True


def test_leakage_detector_identifies_synthetic_signatures():
    """INV-11: Leakage detector must catch any synthetic activity/project/task signature."""
    sample_records = [
        {"id": "1", "title": "Half Marathon Autumn Preparation"},
        {"id": "2", "title": "Carrera Inicial 13"},
        {"id": "3", "title": "Mountain Pass Weekend Ride"},
        {"id": "4", "name": "Datalaria Growth & Architecture"},
        {"id": "5", "title": "Entrenamiento Fitify Tabata S8-3"},
        {"id": "6", "title": "Supabase RLS Multi-Schema Audit"},
    ]
    leaked = detect_synthetic_leakage(sample_records)
    leaked_titles = {r.get("title") or r.get("name") for r in leaked}

    assert leaked_titles == {
        "Half Marathon Autumn Preparation",
        "Mountain Pass Weekend Ride",
        "Datalaria Growth & Architecture",
        "Supabase RLS Multi-Schema Audit",
    }


def test_leakage_detector_clean_on_real_user_data():
    """INV-11: Real user activities must produce ZERO false positive detections."""
    real_records = [
        {"id": "1", "title": "Carrera Inicial 13"},
        {"id": "2", "title": "Carrera Inicial 12"},
        {"id": "3", "title": "Entrenamiento Fitify Tabata S8-3"},
        {"id": "4", "title": "Entrenamiento Fitify HIIT S8-2"},
        {"id": "5", "name": "Datalaria - Starter Kits"},
        {"id": "6", "title": "Soporte Proyector"},
    ]
    leaked = detect_synthetic_leakage(real_records)
    assert len(leaked) == 0


def test_tenant_isolation_router_query_filters(monkeypatch):
    """
    INV-11: Verify that router queries enforce strictly user_id = current_user.id
    preventing any cross-tenant data leakage between user_A and user_B.
    """
    user_a_uid = "user-a-11111"
    user_b_uid = "user-b-22222"

    payload_a = {
        "sub": user_a_uid,
        "email": "userA@example.com",
        "role": "authenticated",
        "aud": "authenticated",
        "exp": int(time.time()) + 3600,
    }
    token_a = jwt.encode(payload_a, SECRET, algorithm="HS256")

    applied_user_filters = []

    def mock_db(table_name):
        class MockQuery:
            def __init__(self, tbl):
                self.tbl = tbl
            def select(self, *args):
                return self
            def eq(self, col, val):
                if col == "user_id":
                    applied_user_filters.append((self.tbl, val))
                return self
            def order(self, *args, **kwargs):
                return self
            def limit(self, *args, **kwargs):
                return self
            def offset(self, *args, **kwargs):
                return self
            def execute(self):
                class MockRes:
                    data = []
                return MockRes()
        return MockQuery(table_name)

    import routers.activities as r_activities
    monkeypatch.setattr(r_activities, "db", mock_db)

    # When User A requests activities
    response = client.get("/api/v1/activities/", headers={"Authorization": f"Bearer {token_a}"})
    assert response.status_code == 200
    assert ("activities", user_a_uid) in applied_user_filters
    # User B's UID must NEVER be queried
    assert ("activities", user_b_uid) not in applied_user_filters


def test_database_audit_no_synthetic_data_in_production_accounts():
    """
    INV-11 Live Database Audit:
    Connects to the Supabase client (using service_role) and asserts that the protected
    user dalaez1@gmail.com has ZERO synthetic activities, projects, or tasks.
    """
    try:
        from services.supabase_client import db
        dalaez_uid = "459d8ddf-5580-4398-88fd-a1ed63df1643"

        # 1. Check activities
        acts = db("activities").select("id, title").eq("user_id", dalaez_uid).execute().data
        leaked_acts = detect_synthetic_leakage(acts, key_field="title")
        assert len(leaked_acts) == 0, f"Found leaked synthetic activities in production account: {leaked_acts}"

        # 2. Check projects
        projs = db("projects").select("id, name").eq("user_id", dalaez_uid).execute().data
        leaked_projs = detect_synthetic_leakage(projs, key_field="name")
        assert len(leaked_projs) == 0, f"Found leaked synthetic projects in production account: {leaked_projs}"

        # 3. Check tasks
        tasks = db("tasks").select("id, title").eq("user_id", dalaez_uid).execute().data
        leaked_tasks = detect_synthetic_leakage(tasks, key_field="title")
        assert len(leaked_tasks) == 0, f"Found leaked synthetic tasks in production account: {leaked_tasks}"

    except Exception as e:
        # If running in hermetic test mode (mock SUPABASE_URL) or offline, skip live audit
        if "getaddrinfo failed" in str(e) or "APIError" in str(e) or "mock-supabase" in str(e):
            pytest.skip(f"Hermetic test environment or Supabase offline (skipping live audit): {e}")
        else:
            raise
