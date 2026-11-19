"""
LifeOps API — Pagination, Embedded Join & Performance Tests (ADR-030)
=====================================================================
Validates SDD Invariants INV-12, INV-13, INV-14, INV-15 and transport headers
(GZipMiddleware + Server-Timing) without requiring live Supabase access.
"""
import datetime as dt
import time
import jwt
import pytest
from fastapi.testclient import TestClient

from main import app
from config import get_settings

client = TestClient(app)

SECRET = "test-secret-key-32-chars-long-minimum!!"
USER_ID = "user-pagination-11111"


@pytest.fixture(autouse=True)
def configure_test_secret(monkeypatch):
    monkeypatch.setattr(get_settings(), "supabase_jwt_secret", SECRET)


def _make_auth_header(user_id: str = USER_ID) -> dict[str, str]:
    token = jwt.encode(
        {
            "sub": user_id,
            "email": "athlete@datalaria.com",
            "role": "authenticated",
            "aud": "authenticated",
            "exp": int(time.time()) + 3600,
        },
        SECRET,
        algorithm="HS256",
    )
    return {"Authorization": f"Bearer {token}"}


def _build_synthetic_sport_rows(n: int = 50) -> list[dict]:
    """
    Generate N deterministic sport rows with intentional repeated dates (3 per date)
    to exercise total-order tie-breakers (date DESC, created_at DESC, id DESC).
    """
    base_date = dt.date(2026, 11, 18)
    rows = []
    for i in range(n):
        day = base_date - dt.timedelta(days=i // 3)
        created = f"{day.isoformat()}T{10 + (i % 3):02d}:{(i * 7) % 60:02d}:00+00:00"
        has_exact_sec = (i % 2 == 0)
        duration_min = 30 + (i % 40)
        exact_sec = duration_min * 60 + 25 if has_exact_sec else None
        rows.append(
            {
                "id": f"act-{i:04d}",
                "user_id": USER_ID,
                "activity_type": "sport",
                "title": f"Session #{i + 1} - Endurance Block",
                "description": f"Detailed workout notes for performance compression testing row {i}",
                "date": day.isoformat(),
                "duration_minutes": duration_min,
                "metadata": {"duration_seconds": exact_sec} if has_exact_sec else {},
                "created_at": created,
                "updated_at": created,
                "workouts": [
                    {
                        "id": f"wrk-{i:04d}",
                        "activity_id": f"act-{i:04d}",
                        "workout_type": "running" if i % 3 != 0 else "gym",
                        "distance_km": round(5.0 + (i % 10) * 0.75, 2) if i % 3 != 0 else None,
                        "calories": 320 + (i % 5) * 45,
                        "avg_heart_rate": 148,
                        "elevation_m": 60,
                        "personal_best": (i % 17 == 0),
                    }
                ],
            }
        )
    return rows


class FakePostgrestHarness:
    """In-memory PostgREST query simulator enforcing INV-12..15."""

    def __init__(self, rows: list[dict], rpc_enabled: bool = True):
        self.rows = rows
        self.rpc_enabled = rpc_enabled
        self.db_calls = 0
        self.rpc_calls = 0
        self.select_clauses: list[str] = []

    def db(self, table_name: str):
        harness = self

        class MockQuery:
            def __init__(self):
                self._table = table_name
                self._filters: list[tuple[str, str, object]] = []
                self._orders: list[tuple[str, bool]] = []
                self._range: tuple[int, int] | None = None
                self._limit: int | None = None
                self._count_mode: str | None = None

            def select(self, clause: str, count: str | None = None):
                harness.select_clauses.append(clause)
                self._count_mode = count
                return self

            def eq(self, col: str, val):
                self._filters.append(("eq", col, val))
                return self

            def gte(self, col: str, val):
                self._filters.append(("gte", col, val))
                return self

            def lte(self, col: str, val):
                self._filters.append(("lte", col, val))
                return self

            def in_(self, col: str, vals):
                raise AssertionError(f"INV-15 violation: .in_({col}, ...) must never be called")

            def order(self, col: str, desc: bool = False):
                self._orders.append((col, desc))
                return self

            def range(self, start: int, end: int):
                self._range = (start, end)
                return self

            def limit(self, n: int):
                self._limit = n
                return self

            def execute(self):
                harness.db_calls += 1
                matched = list(harness.rows)
                for op, col, val in self._filters:
                    if op == "eq":
                        matched = [r for r in matched if r.get(col) == val]
                    elif op == "gte":
                        matched = [r for r in matched if r.get(col, "") >= val]
                    elif op == "lte":
                        matched = [r for r in matched if r.get(col, "") <= val]

                # Apply orders from least significant to most significant (Python Timsort is stable)
                for col, is_desc in reversed(self._orders):
                    matched.sort(key=lambda r: r.get(col, ""), reverse=is_desc)

                total_count = len(matched) if self._count_mode == "exact" else None

                if self._range is not None:
                    start, end = self._range
                    sliced = matched[start : end + 1]
                elif self._limit is not None:
                    sliced = matched[: self._limit]
                else:
                    sliced = matched

                class Res:
                    data = sliced
                    count = total_count

                return Res()

        return MockQuery()

    def rpc(self, fn_name: str, params: dict | None = None):
        harness = self

        class MockRpc:
            def execute(self):
                harness.rpc_calls += 1
                if not harness.rpc_enabled:
                    raise RuntimeError("PGRST202: function lifeops.sport_summary not found")
                uid = (params or {}).get("p_user_id")
                user_rows = [
                    r for r in harness.rows
                    if r["user_id"] == uid and r["activity_type"] == "sport"
                ]
                total_km = round(sum(float(r["workouts"][0]["distance_km"] or 0) for r in user_rows), 2)
                total_kcal = sum(int(r["workouts"][0]["calories"] or 0) for r in user_rows)
                pb_count = sum(1 for r in user_rows if r["workouts"][0]["personal_best"])
                total_sec = sum(
                    int(r["metadata"]["duration_seconds"])
                    if r["metadata"].get("duration_seconds") is not None
                    else r["duration_minutes"] * 60
                    for r in user_rows
                )

                class Res:
                    data = [
                        {
                            "count": len(user_rows),
                            "total_km": total_km,
                            "total_seconds": total_sec,
                            "total_kcal": total_kcal,
                            "pb_count": pb_count,
                        }
                    ]

                return Res()

        return MockRpc()


def test_paged_deterministic_total_order_disjoint_union(monkeypatch):
    """INV-12: All pages are strictly disjoint, ordered deterministically, and their union equals N=50."""
    import routers.activities as r_activities

    rows = _build_synthetic_sport_rows(50)
    harness = FakePostgrestHarness(rows, rpc_enabled=True)
    monkeypatch.setattr(r_activities, "db", harness.db)
    monkeypatch.setattr(r_activities, "rpc", harness.rpc)

    seen_ids: list[str] = []
    seen_sort_keys: list[tuple[str, str, str]] = []

    for page in range(1, 6):
        resp = client.get(
            f"/api/v1/activities/paged?activity_type=sport&page={page}&page_size=12&include_summary=false",
            headers=_make_auth_header(),
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["page"] == page
        assert body["page_size"] == 12
        assert body["total"] == 50
        assert body["total_pages"] == 5
        assert body["has_more"] is (page < 5)
        assert body["summary"] is None

        expected_len = 12 if page < 5 else 2
        assert len(body["items"]) == expected_len

        for item in body["items"]:
            assert "workouts" not in item
            assert isinstance(item["workout"], dict)
            seen_ids.append(item["id"])
            seen_sort_keys.append((item["date"], item["created_at"], item["id"]))

    # Disjoint union == exact 50 IDs
    assert len(seen_ids) == 50
    assert len(set(seen_ids)) == 50
    # Strictly descending total order across page boundaries
    assert seen_sort_keys == sorted(seen_sort_keys, reverse=True)
    # include_summary=false => 5 page queries total, 0 RPC calls
    assert harness.db_calls == 5
    assert harness.rpc_calls == 0


def test_paged_page_size_whitelist_and_validation(monkeypatch):
    """INV-13: Only page_size in {12, 24, 48} is accepted; invalid sizes or page < 1 return 422."""
    import routers.activities as r_activities

    harness = FakePostgrestHarness(_build_synthetic_sport_rows(50), rpc_enabled=True)
    monkeypatch.setattr(r_activities, "db", harness.db)
    monkeypatch.setattr(r_activities, "rpc", harness.rpc)

    for valid_size in (12, 24, 48):
        resp = client.get(
            f"/api/v1/activities/paged?activity_type=sport&page=1&page_size={valid_size}&include_summary=false",
            headers=_make_auth_header(),
        )
        assert resp.status_code == 200
        assert len(resp.json()["items"]) == valid_size

    for invalid_size in (0, 10, 25, 50, 100):
        resp = client.get(
            f"/api/v1/activities/paged?activity_type=sport&page=1&page_size={invalid_size}",
            headers=_make_auth_header(),
        )
        assert resp.status_code == 422

    resp_bad_page = client.get(
        "/api/v1/activities/paged?activity_type=sport&page=0&page_size=12",
        headers=_make_auth_header(),
    )
    assert resp_bad_page.status_code == 422


def test_paged_summary_rpc_and_fallback_match_full_dataset(monkeypatch):
    """INV-14: Summary equals sum across all pages, both via SQL RPC and via Python block fallback."""
    import routers.activities as r_activities

    rows = _build_synthetic_sport_rows(50)

    expected_km = round(sum(float(r["workouts"][0]["distance_km"] or 0) for r in rows), 2)
    expected_kcal = sum(int(r["workouts"][0]["calories"] or 0) for r in rows)
    expected_pb = sum(1 for r in rows if r["workouts"][0]["personal_best"])
    expected_sec = sum(
        int(r["metadata"]["duration_seconds"])
        if r["metadata"].get("duration_seconds") is not None
        else r["duration_minutes"] * 60
        for r in rows
    )

    # 1. SQL RPC path (fast path)
    rpc_harness = FakePostgrestHarness(rows, rpc_enabled=True)
    monkeypatch.setattr(r_activities, "db", rpc_harness.db)
    monkeypatch.setattr(r_activities, "rpc", rpc_harness.rpc)

    r_p1 = client.get(
        "/api/v1/activities/paged?activity_type=sport&page=1&page_size=12&include_summary=true",
        headers=_make_auth_header(),
    )
    assert r_p1.status_code == 200
    s_rpc = r_p1.json()["summary"]
    assert s_rpc == {
        "count": 50,
        "total_km": expected_km,
        "total_seconds": expected_sec,
        "total_kcal": expected_kcal,
        "pb_count": expected_pb,
    }
    assert rpc_harness.rpc_calls == 1
    assert rpc_harness.db_calls == 1

    # 2. Fallback block-aggregator path (if RPC not yet deployed in Supabase)
    fb_harness = FakePostgrestHarness(rows, rpc_enabled=False)
    monkeypatch.setattr(r_activities, "db", fb_harness.db)
    monkeypatch.setattr(r_activities, "rpc", fb_harness.rpc)

    r_p3 = client.get(
        "/api/v1/activities/paged?activity_type=sport&page=3&page_size=12&include_summary=true",
        headers=_make_auth_header(),
    )
    assert r_p3.status_code == 200
    assert r_p3.json()["summary"] == s_rpc


def test_server_timing_and_gzip_compression(monkeypatch):
    """ADR-030: Backend exposes Server-Timing header and compresses payloads > 1024 bytes with gzip."""
    import routers.activities as r_activities

    harness = FakePostgrestHarness(_build_synthetic_sport_rows(50), rpc_enabled=True)
    monkeypatch.setattr(r_activities, "db", harness.db)
    monkeypatch.setattr(r_activities, "rpc", harness.rpc)

    resp = client.get(
        "/api/v1/activities/paged?activity_type=sport&page=1&page_size=24&include_summary=true",
        headers={**_make_auth_header(), "Accept-Encoding": "gzip"},
    )
    assert resp.status_code == 200
    assert "server-timing" in resp.headers
    assert "app;dur=" in resp.headers["server-timing"]
    assert resp.headers.get("content-encoding") == "gzip"
