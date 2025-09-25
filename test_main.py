import pytest
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_upload_image():
    response = client.post("/caption/", content = open("images/forest.jpg", "rb"))
    print(response.json())
