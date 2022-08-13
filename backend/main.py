from datetime import datetime
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

import re
import json

from database import SessionLocal
import models

app = FastAPI()

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


class User(BaseModel):
    id: Optional[int]
    username: str
    hasAdmin: bool
    teamID: int

    class Config:
        orm_mode = True


class Team(BaseModel):
    id: Optional[int]
    teamname: str
    users: Optional[List[User]]

    class Config:
        orm_mode = True


class Entry(BaseModel):
    id: int
    # date: str
    time_in: Optional[datetime]
    time_out: Optional[datetime]
    timesheetID: int

    class Config:
        orm_mode = True


class Timesheet(BaseModel):
    id: int
    owner: User
    times: Optional[List[Entry]]

    class Config:
        orm_mode = True


db = SessionLocal()


@app.get('/')
def responding():
    return "API is responding"

# User endpoints ------------------


@app.get('/users', response_model=List[User], status_code=status.HTTP_200_OK)
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
def create_user(user: User):
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


@app.put('/user/{user_id}', response_model=User, status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id: int, new_user: User):
    user = db.query(models.User).filter(models.User.id == user_id).first()
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

    db.delete(user)
    db.commit

    return (user)


# Team endpoints ------------------

@app.get('/teams', response_model=List[Team], status_code=status.HTTP_200_OK)
def get_teams():
    teams = db.query(models.Team).all()
    return teams


@app.get('/team/{team_id}', response_model=Team, status_code=status.HTTP_200_OK)
def get_team(team_id: int):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found.")
    return team


@app.post('/team', response_model=Team, status_code=status.HTTP_201_CREATED)
def create_team(team: Team):
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

    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found.")

    db.delete(team)
    db.commit()

    return (team)

# Timesheet endpoints ------------------


@app.get("/timesheets", response_model=List[Timesheet], status_code=status.HTTP_200_OK)
def get_timesheets():
    timesheets = db.query(models.Timesheet).all()
    return timesheets


@app.get("/timesheet/{timesheet_id}", response_model=Timesheet)
def get_timesheet(timesheet_id: int):
    timesheet = db.query(models.Timesheet).filter(
        models.Timesheet.id == timesheet_id).first()
    if timesheet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Timesheet not found.")
    return timesheet


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


@app.get("/entries", response_model=List[Entry], status_code=status.HTTP_200_OK)
def get_entries():
    entries = db.query(models.Entry).all()
    return entries


@app.get("/entry/{entry_id}", response_model=Entry, status_code=status.HTTP_200_OK)
def get_entry(entry_id: int):
    entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Entry does not exist.")
    return (entry)


@app.post("/clock-in", response_model=Entry, status_code=status.HTTP_202_ACCEPTED)
def clock_in(entry: Entry):
    if entry.time_in is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No clock-in time provided")
    timesheet = db.query(models.Timesheet).filter(
        models.Timesheet.id == entry.timesheetID).first()
    date = entry.time_in.strftime("%x")
    # serach for clock-in date in existing records
    if re.search('"date": {date}', json.dumps(timesheet.times), re.M):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You have already clocked in today.")

    new_entry = models.Entry(
        date=date,
        time_in=entry.time_in,
        time_out=None,
        timesheetID=entry.timesheetID
    )

    db.add(new_entry)
    db.commit()

    return new_entry


@app.put("/clock-out", response_model=Entry, status_code=status.HTTP_200_OK)
def clock_out(new_entry: Entry):
    if entry.time_out is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No clock-out time provided")

    entry = db.query(models.Entry).filter(models.Entry.date ==
                                          new_entry.time_out.strftime("%x")).first()

    # If time_out already exists
    if entry.time_out is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You have already clocked out today.")

    entry.time_out = new_entry.time_out

    db.commit()

    return entry
