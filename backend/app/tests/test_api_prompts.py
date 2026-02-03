from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_list_prompts(client):
    r = client.post("/api/prompts", json={"name": "Test Prompt", "description": "Desc"})
    assert r.status_code == 201

    r2 = client.get("/api/prompts")
    assert r2.status_code == 200
    assert any(p["name"] == "Test Prompt" for p in r2.json())

