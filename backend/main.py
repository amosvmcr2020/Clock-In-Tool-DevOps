from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

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
def create_user(user:User):
    check_user = db.query(models.User).filter(models.User.username == user.username).first()
    check_team = db.query(models.Team).filter(models.Team.id == user.teamID).first()

    if check_user is not None: 
        raise HTTPException(status_code=400, detail="This username is already in use.")
    
    if check_team is None: 
        raise HTTPException(status_code=400, detail="This team does not exist")

    new_user = models.User(
        username = user.username,
        hasAdmin = user.hasAdmin,
        teamID = user.teamID
    )

    db.add(new_user)
    db.commit()

    return new_user

@app.put('/user/{user_id}', response_model=User, status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id:int, new_user:User):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user.username = new_user.username
    user.hasAdmin = new_user.hasAdmin
    user.teamID = new_user.teamID

    db.commit()

    return(user)

@app.delete('/user/{user_id}', response_model=User, status_code=status.HTTP_202_ACCEPTED)
def delete_user(user_id:int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None: 
        raise HTTPException(status_code=404, detail="User does not exist.")

    db.delete(user)
    db.commit

    return(user)


# Team endpoints ------------------

@app.get('/teams', response_model=List[Team], status_code=status.HTTP_200_OK)
def get_teams():
    teams = db.query(models.Team).all()
    return teams

@app.get('/team/{team_id}', response_model=Team, status_code=status.HTTP_200_OK)
def get_team(team_id:int):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    return team

@app.post('/team', response_model=Team, status_code=status.HTTP_201_CREATED)
def create_team(team:Team): 
    check_team = db.query(models.Team).filter(models.Team.teamname ==  team.teamname).first()

    if check_team is not None: 
        raise HTTPException(status_code=400, detail="This team already exists.")

    new_team = models.Team(
        teamname = team.teamname
    )

    db.add(new_team)
    db.commit()

    return new_team

@app.put('/team/{team_id}', response_model=Team, status_code=status.HTTP_202_ACCEPTED)
def update_team(team_id:int, new_team:Team):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()

    if team is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found.")

    team.teamname = new_team.teamname

    db.commit()

    return(team)

@app.delete('/team/{team_id}', response_model=Team, status_code=status.HTTP_202_ACCEPTED)
def delete_team(team_id:int):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found.")

    db.delete(team)
    db.commit()

    return(team)
    