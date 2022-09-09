from venv import create
from fastapi.testclient import TestClient
from .main import app
from .create_db import create_new_db

client = TestClient(app)

create_new_db()


def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "API is responding"


def test_read_users():
    response = client.get("/user")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "username": "Administrator",
            "hasAdmin": True,
            "teamID": 1
        },
        {
            "id": 2,
            "username": "John",
            "hasAdmin": False,
            "teamID": 2
        },
        {
            "id": 3,
            "username": "TeamLeader",
            "hasAdmin": True,
            "teamID": 2
        }
    ]


def test_read_user():
    response = client.get("/user/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "username": "Administrator",
        "hasAdmin": True,
        "teamID": 1
    }


def test_bad_read_user():
    response = client.get("/user/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "User does not exist"}


def test_create_user():
    response = client.post(
        "/user",
        json={"username": "new_user", "password": "p4ssw0rd",
              "hasAdmin": False, "teamID": 1},
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 4,
        "username": "new_user",
        "hasAdmin": False,
        "teamID": 1
    }
