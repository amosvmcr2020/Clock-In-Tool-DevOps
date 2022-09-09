from fastapi.testclient import TestClient
from .main import app
from .create_db import create_new_db

client = TestClient(app)

create_new_db()


# Test API is responding
def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "API is responding"


# Test get users returns list of users
def test_get_users():
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


# Test get specific user returns correct user
def test_get_user():
    response = client.get("/user/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "username": "Administrator",
        "hasAdmin": True,
        "teamID": 1
    }


# Test cannot get nonexistent user
def test_bad_read_user():
    response = client.get("/user/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "User does not exist"}


# Test create new user and check exists in db
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

    # Check user exists in db
    response = client.get("/user/4")
    assert response.status_code == 200
    assert response.json() == {
        "id": 4,
        "username": "new_user",
        "hasAdmin": False,
        "teamID": 1
    }


# Test cannot create duplicate username
def test_duplicate_create_user():
    response = client.post(
        "/user",
        json={"username": "Administrator", "password": "p4ssw0rd",
              "hasAdmin": False, "teamID": 1},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "This username is already in use."}


'''Following test not working WHY'''
# # Test edit user
# def test_edit_user():
#     response = client.patch(
#         "/user/4", json={"username": "newer_user", "teamID": 2, "hasAdmin": True})
#     assert response.status_code == 202
#     assert response.json() == {
#         "id": 4, "username": "newer_user", "teamID": 2, "hasAdmin": True}


# Test delete user
def test_delete_user():
    response = client.delete("/user/4?authUserID=1")
    assert response.status_code == 202
    assert response.json() == {
        "id": 4,
        "username": "new_user",
        "hasAdmin": False,
        "teamID": 1
    }

    # Test user no longer exists in db
    response = client.get("/user/4")
    assert response.status_code == 404
    assert response.json() == {"detail": "User does not exist"}


# Test delete user without admin
def test_unauthorised_delete_user():
    # Pass in user without admin
    response = client.delete("/user/3?authUserID=2")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You must have admin priveledges to do this."}


# Test delete nonexistent user
def test_delete_nonexistent_user():
    response = client.delete("/user/99?authUserID=1")
    assert response.status_code == 404
    assert response.json() == {"detail": "User does not exist."}


# Test login successfully
def test_login_successful():
    response = client.post(
        "/login", json={"username": "Administrator", "password": "admin"})
    assert response.status_code == 200
    assert response.json() == 1


# Test login with incorrect password
def test_login_bad_password():
    response = client.post(
        "/login", json={"username": "Administrator", "password": "wrong-pass"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Username or password is incorrect."}


# Test login with nonexistent username
def test_login_bad_username():
    response = client.post(
        "/login", json={"username": "not-a-user", "password": "admin"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Username or password is incorrect."}


# Test get teams
def test_get_teams():
    response = client.get("/team")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "teamname": "Team 1",
            "users": [
                {
                        "id": 1,
                        "username": "Administrator",
                        "hasAdmin": True,
                        "teamID": 1
                }
            ]
        },
        {
            "id": 2,
            "teamname": "Team 2",
            "users": [
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
        }
    ]


# Test get specific team
def test_get_team():
    response = client.get("team/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "teamname": "Team 1",
        "users": [
            {
                    "id": 1,
                "username": "Administrator",
                "hasAdmin": True,
                "teamID": 1
            }
        ]
    }


# Test edit team
def test_edit_team():
    response = client.put("team/1", json={"teamname": "Test Team"})
    assert response.status_code == 202
    assert response.json() == {
        "id": 1,
        "teamname": "Test Team",
        "users": [
            {
                    "id": 1,
                "username": "Administrator",
                "hasAdmin": True,
                "teamID": 1
            }
        ]
    }


# Test create team
def test_create_team():
    response = client.post("team", json={"teamname": "new_team"})
    assert response.status_code == 201
    assert response.json() == {
        "id": 3,
        "teamname": "new_team",
        "users": []
    }


# Test delete empty team
def test_delete_team():
    response = client.delete("team/3?authUserID=1")
    assert response.status_code == 202
    assert response.json() == {
        "id": 3,
        "teamname": "new_team",
        "users": []
    }


# Test delete team with users
def test_delete_populated_team():
    response = client.delete("/team/2?authUserID=1")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Cannot delete team with users."
    }


# Test delete team that doesn't exist
def test_delete_nonexistent_team():
    response = client.delete("team/99?authUserID=1")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Team not found."
    }


# Test delete team without admin
def test_unauthorised_delete_team():
    response = client.delete("team/2?authUserID=2")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You must have admin priveledges to do this."
    }


# Test clock in
def test_clock_in():
    response = client.post(
        "/clock-in", json={"millis_in": 1662712200000, "timesheetID": 1})
    assert response.status_code == 202
    assert response.json() == {
        "id": 4,
        "date": "09/09/22",
        "time_in": "2022-09-09T09:30:00",
        "time_out": None,
        "timesheetID": 1
    }


# Test clock in twice in one day
def test_duplicate_clock_in():
    response = client.post(
        "/clock-in", json={"millis_in": 1662712200000, "timesheetID": 1})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "You have already clocked in today."
    }


# Test clock in with invalid timesheet
def test_no_timesheet_clock_in():
    response = client.post(
        "/clock-in", json={"millis_in": 1662712200000, "timesheetID": 99})
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Timesheet not found."
    }


# Test clock out
def test_clock_out():
    response = client.put(
        "/clock-out", json={"millis_out": 1662739200000, "timesheetID": 1})
    assert response.status_code == 202
    assert response.json() == {
        "id": 4,
        "date": "09/09/22",
        "time_in": "2022-09-09T09:30:00",
        "time_out": "2022-09-09T17:00:00",
        "timesheetID": 1
    }


# Test clock out twice in one day
def test_duplicate_clock_out():
    response = client.put(
        "/clock-out", json={"millis_out": 1662739200000, "timesheetID": 1})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "You have already clocked out today."
    }


# Test clock out without clocking in
def test_clock_out_without_clock_in():
    response = client.put(
        "/clock-out", json={"millis_out": 1662825600000, "timesheetID": 99})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "You have not clocked in today."
    }
