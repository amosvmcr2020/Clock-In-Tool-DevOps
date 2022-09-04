import hashlib

from datetime import datetime
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from schemas import *

from database import SessionLocal
import models

app = FastAPI(title="Clock In API", swagger_ui_parameters={
              "operationsSorter": "method"})

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


db = SessionLocal()


def hashFunc(password):
    return hashlib.sha1(password.encode("UTF-8")).hexdigest()


@app.get('/')
def responding():
    return "API is responding"

# User endpoints ------------------


@app.get('/user', response_model=List[User], status_code=status.HTTP_200_OK)
def get_users():
    users = db.query(models.User).all()
    return users


@app.get('/user/{user_id}', response_model=User, status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return user


@app.post('/user', response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserIn):

    if user.username == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username cannot be empty")
    if user.password == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password cannot be empty")

    check_user = db.query(models.User).filter(
        models.User.username == user.username).first()
    check_team = db.query(models.Team).filter(
        models.Team.id == user.teamID).first()

    if check_user is not None:
        raise HTTPException(
            status_code=400, detail="This username is already in use.")

    if check_team is None:
        raise HTTPException(status_code=400, detail="This team does not exist")

    new_user = models.User(
        username=user.username,
        hashed_password=hashFunc(user.password),
        hasAdmin=user.hasAdmin,
        teamID=user.teamID
    )

    new_timesheet = models.Timesheet(
        owner=new_user,
    )

    db.add(new_user)
    db.add(new_timesheet)
    db.commit()

    return new_user


@app.get('/user/{user_id}/timesheet', response_model=int, status_code=status.HTTP_200_OK)
def get_user_timesheet(user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist.")

    timesheet = db.query(models.Timesheet).filter(
        models.Timesheet.owner == user).first()
    if timesheet is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not have a timesheet."
        )
    timesheet_id = timesheet.id
    return timesheet_id


@app.get('/user/{user_id}/timesheet/summary', response_model=Timesheet, status_code=status.HTTP_200_OK)
def get_user_timesheet(user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist.")

    timesheet = db.query(models.Timesheet).filter(
        models.Timesheet.owner == user).first()
    if timesheet is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not have a timesheet."
        )
    return timesheet


@app.patch('/user/{user_id}', response_model=User, status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id: int, new_user: User):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    check_user = db.query(models.User).filter(
        models.User.username == new_user.username).first()
    if check_user is not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This username is already taken")
    user.username = new_user.username
    user.hasAdmin = new_user.hasAdmin
    user.teamID = new_user.teamID

    db.commit()

    return user


@app.delete('/user/{user_id}', response_model=User, status_code=status.HTTP_202_ACCEPTED)
def delete_user(user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist.")

    timesheet = db.query(models.Timesheet).filter(
        models.Timesheet.owner == user).first()

    db. delete(timesheet)

    db.delete(user)
    db.commit

    return (user)


@app.post('/login', status_code=status.HTTP_200_OK)
def user_login(user: UserLogin):
    check_user = db.query(models.User).filter(
        models.User.username == user.username).first()
    if check_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username or password is incorrect.")
    if hashFunc(user.password) == check_user.hashed_password:
        return check_user.id
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Username or password is incorrect.")


# Team endpoints ------------------


@app.get('/team', response_model=List[Team], status_code=status.HTTP_200_OK)
def get_teams():
    teams = db.query(models.Team).all()
    return teams


# Not used
@app.get('/team/{team_id}', response_model=Team, status_code=status.HTTP_200_OK)
def get_team(team_id: int):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found.")
    return team


@app.post('/team', response_model=Team, status_code=status.HTTP_201_CREATED)
def create_team(team: Team):

    if team.teamname == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Team name cannot be empty")

    check_team = db.query(models.Team).filter(
        models.Team.teamname == team.teamname).first()

    if check_team is not None:
        raise HTTPException(
            status_code=400, detail="This team already exists.")

    new_team = models.Team(
        teamname=team.teamname
    )

    db.add(new_team)
    db.commit()

    return new_team


# Not used
@app.put('/team/{team_id}', response_model=Team, status_code=status.HTTP_202_ACCEPTED)
def update_team(team_id: int, new_team: Team):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()

    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found.")

    team.teamname = new_team.teamname

    db.commit()

    return (team)


@app.delete('/team/{team_id}', response_model=Team, status_code=status.HTTP_202_ACCEPTED)
def delete_team(team_id: int):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()

    if team.users != []:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Cannot delete team with users.")

    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found.")

    db.delete(team)
    db.commit()

    return (team)

# Timesheet endpoints ------------------


# Not used
@app.get("/timesheet", response_model=List[Timesheet], status_code=status.HTTP_200_OK)
def get_timesheets():
    timesheets = db.query(models.Timesheet).all()
    return timesheets

# Not used


@app.get("/timesheet/{timesheet_id}", response_model=Timesheet)
def get_timesheet(timesheet_id: int):
    timesheet = db.query(models.Timesheet).filter(
        models.Timesheet.id == timesheet_id).first()
    if timesheet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Timesheet not found.")
    return timesheet

# Not used


@app.get("/timesheet/user/{user_id}", response_model=Timesheet)
def get_user_timesheet(user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    timesheet = user.timesheet
    return timesheet

# Is this still needed?


# Not used
@app.post("/timesheet", response_model=Timesheet, status_code=status.HTTP_202_ACCEPTED)
def create_timesheet(timesheet: Timesheet, ):
    check_timesheet = db.query(models.Timesheet).filter(
        models.Timesheet.owner == timesheet.owner).first()
    if check_timesheet is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Timesheet already exists.")

    new_timesheet = models.Timesheet(
        owner=timesheet.owner,
    )

    db.add(new_timesheet)
    db.commit()

    return (new_timesheet)

# Entry endpoints ------------------


# Not used
@app.get("/entry", response_model=List[Entry], status_code=status.HTTP_200_OK)
def get_entries():
    entries = db.query(models.Entry).all()
    return entries


# Not used
@app.get("/entry/{entry_id}", response_model=Entry, status_code=status.HTTP_200_OK)
def get_entry(entry_id: int):
    entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Entry does not exist.")
    return (entry)


@app.post("/clock-in", response_model=Entry, status_code=status.HTTP_202_ACCEPTED)
def clock_in(entry: Clock_req):
    if entry.millis_in:
        time_in = datetime.fromtimestamp(entry.millis_in/1000.0)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No clock-in time provided")
    if time_in is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No clock-in time provided")
    timesheet = db.query(models.Timesheet).filter(
        models.Timesheet.id == entry.timesheetID).first()
    date = time_in.strftime("%x")
    # serach for clock-in date in existing records
    if any(entry.date == date for entry in timesheet.times):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You have already clocked in today.")

    new_entry = models.Entry(
        date=date,
        time_in=time_in,
        time_out=None,
        timesheetID=entry.timesheetID
    )

    db.add(new_entry)
    db.commit()

    return new_entry


@app.put("/clock-out", response_model=Entry, status_code=status.HTTP_200_OK)
def clock_out(new_entry: Clock_req):

    if new_entry.millis_out:
        time_out = datetime.fromtimestamp(
            new_entry.millis_out/1000.0)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No clock-out time provided")
    if time_out is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No clock-out time provided")

    entry = db.query(models.Entry).filter(models.Entry.timesheetID == new_entry.timesheetID).filter(
        models.Entry.date == time_out.strftime("%x")).first()

    if entry is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You have not clocked in today.")

    # If time_out already exists
    if entry.time_out is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You have already clocked out today.")

    entry.time_out = time_out

    db.commit()

    return entry
