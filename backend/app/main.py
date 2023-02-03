import hashlib

from datetime import datetime
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from . import schemas, database, models, create_test_db

app = FastAPI(title="Clock In API")

origins = [
    "http://0.0.0.0:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


db = database.SessionLocal()

create_test_db.create_new_db()


def hashFunc(password):
    return hashlib.sha1(password.encode("UTF-8")).hexdigest()


def checkAdmin(userID):
    user = db.query(models.User).filter(models.User.id == userID).first()
    return user.hasAdmin


@app.get('/')
def responding():
    return "API is responding"


# User endpoints ------------------
# Returns array of Users
@app.get('/user', response_model=List[schemas.User], status_code=status.HTTP_200_OK)
def get_users():
    users = db.query(models.User).all()
    return users


# Returns user according to user_id
@app.get('/user/{user_id}', response_model=schemas.User, status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return user


# Creates user and returns created user
@app.post('/user', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserIn):
    # If username is empty, reject.
    if user.username == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username cannot be empty")
    # If password is empty, reject.
    if user.password == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password cannot be empty")
    check_user = db.query(models.User).filter(
        models.User.username == user.username).first()
    check_team = db.query(models.Team).filter(
        models.Team.id == user.teamID).first()

    # If username in use, reject.
    if check_user is not None:
        raise HTTPException(
            status_code=400, detail="This username is already in use.")

    # If team id does not exist.
    if check_team is None:
        raise HTTPException(status_code=400, detail="This team does not exist")

    new_user = models.User(
        username=user.username,
        hashed_password=hashFunc(user.password),
        hasAdmin=user.hasAdmin,
        teamID=user.teamID
    )

    # Create a timesheet that belongs to the user.
    new_timesheet = models.Timesheet(
        owner=new_user,
    )

    db.add(new_user)
    db.add(new_timesheet)
    db.commit()

    return new_user


# Get the timesheetID of the timesheet belonging to the requested user
@app.get('/user/{user_id}/timesheet', response_model=int, status_code=status.HTTP_200_OK)
def get_user_timesheet(user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist.")

    timesheet = db.query(models.Timesheet).filter(
        models.Timesheet.owner == user).first()
    if timesheet is None:
        # If the user doesn't have a timesheet, create one.
        timesheet = models.Timesheet(owner=user)
    timesheet_id = timesheet.id
    return timesheet_id

# Get the timesheet belonging to the requested user


@app.get('/user/{user_id}/timesheet/summary', response_model=schemas.Timesheet, status_code=status.HTTP_200_OK)
def get_user_timesheet_summary(user_id: int):
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


# Update the requested user
@app.patch('/user/{user_id}', response_model=schemas.User, status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id: int, new_user: schemas.User):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    check_user = db.query(models.User).filter(
        models.User.username == new_user.username).first()
    if check_user is not None and check_user is not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This username is already taken")
    user.username = new_user.username
    user.hasAdmin = new_user.hasAdmin
    user.teamID = new_user.teamID

    db.commit()

    return user


# Delete the requested user
@app.delete('/user/{user_id}', response_model=schemas.User, status_code=status.HTTP_202_ACCEPTED)
def delete_user(user_id: int, authUserID: int):

    if not checkAdmin(authUserID):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You must have admin priveledges to do this.")
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist.")

    timesheet = db.query(models.Timesheet).filter(
        models.Timesheet.owner == user).first()

    db. delete(timesheet)

    db.delete(user)
    db.commit

    return (user)


# Endpoint to check if queried user is currently online
@app.get('/user/{user_id}/online', response_model=bool, status_code=status.HTTP_200_OK)
def check_online(user_id):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    timesheet = db.query(models.Timesheet).filter(
        models.Timesheet.owner == user).first()
    date = datetime.now().strftime("%x")
    entry = db.query(models.Entry).filter(models.Entry.timesheetID ==
                                          timesheet.id).filter(models.Entry.date == date).first()
    if entry is not None:
        if entry.time_out is None:
            return True
    return False


# Endpoint used to validate login credentials
@app.post('/login', status_code=status.HTTP_200_OK)
def user_login(user: schemas.UserLogin):
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

# Get a list of teams
@app.get('/team', response_model=List[schemas.Team], status_code=status.HTTP_200_OK)
def get_teams():
    teams = db.query(models.Team).order_by(models.Team.teamname.asc()).all()
    return teams


# Get a specific team
@app.get('/team/{team_id}', response_model=schemas.Team, status_code=status.HTTP_200_OK)
def get_team(team_id: int):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found.")
    return team


# Create a new team
@app.post('/team', response_model=schemas.Team, status_code=status.HTTP_201_CREATED)
def create_team(team: schemas.Team):
    # Ensure teamname is not empty
    if team.teamname == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Team name cannot be empty")

    check_team = db.query(models.Team).filter(
        models.Team.teamname == team.teamname).first()
    # Ensure teamname is not in use
    if check_team is not None:
        raise HTTPException(
            status_code=400, detail="This team already exists.")

    new_team = models.Team(
        teamname=team.teamname
    )

    db.add(new_team)
    db.commit()

    return new_team


# Get the team that the requested user belongs to
@app.get('/team/user/{user_id}', response_model=schemas.Team, status_code=status.HTTP_200_OK)
def get_user_team(user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    team = db.query(models.Team).filter(models.Team.id == user.teamID).first()
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found."
        )
    return team


# Update the requested team with a new name
@app.patch('/team/{team_id}', response_model=schemas.Team, status_code=status.HTTP_202_ACCEPTED)
def update_team(team_id: int, new_team: schemas.Team):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()

    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found.")
    # Ensure the teamname is not already in use
    check_team = db.query(models.Team).filter(
        models.Team.teamname == new_team.teamname).first()
    if check_team is not None and check_team is not team:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Team name already in use.")

    team.teamname = new_team.teamname

    db.commit()

    return (team)


# Delete the requested team
@app.delete('/team/{team_id}', response_model=schemas.Team, status_code=status.HTTP_202_ACCEPTED)
def delete_team(team_id: int, authUserID: int):
    if not checkAdmin(authUserID):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You must have admin priveledges to do this.")

    team = db.query(models.Team).filter(models.Team.id == team_id).first()

    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found.")
    # Do not allow a user to be left without a team
    if team.users != []:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Cannot delete team with users.")

    db.delete(team)
    db.commit()

    return (team)

# Timesheet endpoints ------------------


# Get the list of timesheets
@app.get("/timesheet", response_model=List[schemas.Timesheet], status_code=status.HTTP_200_OK)
def get_timesheets():
    timesheets = db.query(models.Timesheet).all()
    return timesheets


# Get a specific timesheet
@app.get("/timesheet/{timesheet_id}", response_model=schemas.Timesheet)
def get_timesheet(timesheet_id: int):
    timesheet = db.query(models.Timesheet).filter(
        models.Timesheet.id == timesheet_id).first()
    if timesheet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Timesheet not found.")
    return timesheet


# Create a new timesheet
@app.post("/timesheet", response_model=schemas.Timesheet, status_code=status.HTTP_202_ACCEPTED)
def create_timesheet(timesheet: schemas.Timesheet):
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

# Delete the requested timesheet


@app.delete("/timesheet/{timesheet_id}", response_model=schemas.Timesheet, status_code=status.HTTP_202_ACCEPTED)
def delete_timesheet(timesheet_id: int, authUserID: int):
    if not checkAdmin(authUserID):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You must have admin priveledges to do this.")
    timesheet = db.query(models.Timesheet).filter(
        models.Timesheet.id == timesheet_id).first()
    if timesheet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Timesheet not found.")
    db.delete(timesheet)
    db.commit()
    return timesheet


# Delete all entries within the requested timesheet
@app.delete("/timesheet/{timesheet_id}/clear", response_model=List[schemas.Entry], status_code=status.HTTP_202_ACCEPTED)
def clear_timesheet(timesheet_id: int, authUserID: int):
    if not checkAdmin(authUserID):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You must have admin priveledges to do this.")
    entries = db.query(models.Entry).filter(
        models.Entry.timesheetID == timesheet_id).all()
    print(entries)
    for entry in entries:
        db.delete(entry)
    db.commit()
    return entries

# Entry endpoints ------------------


# Get the list of entries
@app.get("/entry", response_model=List[schemas.Entry], status_code=status.HTTP_200_OK)
def get_entries():
    entries = db.query(models.Entry).all()
    return entries


# Get a specific entry
@app.get("/entry/{entry_id}", response_model=schemas.Entry, status_code=status.HTTP_200_OK)
def get_entry(entry_id: int):
    entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Entry does not exist.")
    return (entry)


# Clock in endpoint
@app.post("/clock-in", response_model=schemas.Entry, status_code=status.HTTP_202_ACCEPTED)
def clock_in(entry: schemas.Clock_req):
    if entry.millis_in:
        # Convert to readable datetime
        time_in = datetime.fromtimestamp(entry.millis_in/1000.0)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No clock-in time provided")
    # Ensure the time_in value is assigned properly
    if time_in is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No clock-in time provided")
    timesheet = db.query(models.Timesheet).filter(
        models.Timesheet.id == entry.timesheetID).first()

    if timesheet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Timesheet not found.")

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


# Clock out endpoint
@app.patch("/clock-out", response_model=schemas.Entry, status_code=status.HTTP_202_ACCEPTED)
def clock_out(new_entry: schemas.Clock_req):
    if new_entry.millis_out:
        # Convert to a readable datetime
        time_out = datetime.fromtimestamp(
            new_entry.millis_out/1000.0)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No clock-out time provided")
    # Ensure time_out is assigned properly
    if time_out is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No clock-out time provided")

    # Get the corresponding entry
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
