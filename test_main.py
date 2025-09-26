import os
import json
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

images_path = "images"
server_path = "http://127.0.0.1:8000/"

def get_image_urls(name):
    return f"{server_path}/{name}"

def get_image_names(directory):
  image_names = []

  for filename in os.listdir(directory):
    image_names.append(filename)

  return image_names


def test_organize_images_success():
    image_names = get_image_names(images_path)
    image_urls = [server_path + name for name in image_names]
    response = client.post("/organize/", json = {"urls": image_urls})
    data = response.json()
    print(json.dumps(data, indent = 2, sort_keys = True))    
    assert response.status_code == 200
