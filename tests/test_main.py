import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_add():
    response = client.get("/add/2/3")
    assert response.status_code == 200
    assert response.json() == 5
