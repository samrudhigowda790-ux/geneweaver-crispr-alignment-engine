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

def test_fasta_upload_single_sequence():
    response = client.post(
        "/api/fasta",
        files={
            "file": (
                "sample.fasta",
                b">sequence_1\nATCGATCG\n",
                "text/plain"
            )
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["sequence_count"] == 1
    assert data["sequences"][0]["id"] == "sequence_1"
    assert data["sequences"][0]["sequence"] == "ATCGATCG"


def test_fasta_upload_multiple_sequences():
    response = client.post(
        "/api/fasta",
        files={
            "file": (
                "multiple.fasta",
                b">seq1\nATCG\n>seq2\nGCTA\n",
                "text/plain"
            )
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["sequence_count"] == 2
    assert data["sequences"][0]["sequence"] == "ATCG"
    assert data["sequences"][1]["sequence"] == "GCTA"


def test_fasta_upload_unsupported_extension():
    response = client.post(
        "/api/fasta",
        files={
            "file": ("sample.txt", b">seq1\nATCG\n", "text/plain")
        }
    )

    assert response.status_code == 400


def test_fasta_upload_invalid_dna():
    response = client.post(
        "/api/fasta",
        files={
            "file": ("invalid.fasta", b">seq1\nATCX\n", "text/plain")
        }
    )

    assert response.status_code == 422


def test_fasta_upload_empty_file():
    response = client.post(
        "/api/fasta",
        files={
            "file": ("empty.fasta", b"", "text/plain")
        }
    )

    assert response.status_code == 400

def test_fasta_upload_exceeds_size_limit():
    oversized_content = b">seq1\n" + b"A" * (5 * 1024 * 1024)

    response = client.post(
        "/api/fasta",
        files={
            "file": (
                "large.fasta",
                oversized_content,
                "text/plain"
            )
        }
    )

    assert response.status_code == 413
    assert "exceeds the maximum allowed size" in response.json()["detail"]

