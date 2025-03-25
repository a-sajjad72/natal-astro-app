import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home_route():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.text  # Adjust based on actual content in the template

def test_template_rendering():
    response = client.get("/")
    assert response.status_code == 200
    assert "Expected Content" in response.text  # Replace with actual expected content from the template