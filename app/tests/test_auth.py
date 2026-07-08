from fastapi.testclient import TestClient
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #subir de nivel

from main import app

client = TestClient(app)

def test_login_invalido():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@example.com", # usuario existente en la bd
            "password": "1234" # forzamos fallo en test ya que la contraseña es '123'
        })
    assert response.status_code == 401

def test_ping_docs():
    response = client.get("/docs")
    assert response.status_code == 200