from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_unknown_route_uses_consistent_error_format() -> None:
    response = client.get("/does-not-exist")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"
    assert "message" in response.json()["error"]
