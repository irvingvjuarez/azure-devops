from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_item():
    response = client.post("/items", json={"name": "Test Item", "description": "Test Desc"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test Item"


def test_get_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_single_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_update_item():
    response = client.put("/items/1", json={"name": "Updated", "description": "Updated Desc"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"


def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == 204
