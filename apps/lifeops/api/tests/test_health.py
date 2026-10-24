"""
LifeOps API — Health & System Tests
====================================
Verifies that the API entrypoint and healthcheck endpoints
are operational without requiring live cloud databases.
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "LifeOps API" in data["app"]


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "LifeOps" in data["engine"]
    assert data["schema"] == "lifeops"
