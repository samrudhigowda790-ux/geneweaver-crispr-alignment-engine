from fastapi.testclient import TestClient
from geneweaver.api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_alignment_endpoint():
    response = client.post(
        "/api/align",
        json={"sequence_a": "ATCG", "sequence_b": "ATCG"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["alignment_score"] == 8
    assert data["verified_score"] == 8


def test_alignment_with_mismatch():
    response = client.post(
        "/api/align",
        json={"sequence_a": "ATCG", "sequence_b": "ATGG"}
    )

    assert response.status_code == 200
    assert response.json()["alignment_score"] == 5


def test_invalid_sequence():
    response = client.post(
        "/api/align",
        json={"sequence_a": "ATCX", "sequence_b": "ATCG"}
    )

    assert response.status_code == 422


def test_empty_sequence():
    response = client.post(
        "/api/align",
        json={"sequence_a": "", "sequence_b": "ATCG"}
    )

    assert response.status_code == 422
