from database import Base, engine
import models
from database import SessionLocal
import hashlib


def hashFunc(password):
    return hashlib.sha1(password.encode("UTF-8")).hexdigest()


print("Dropping existing database...")
Base.metadata.drop_all(engine)

print("Creating Database...")
Base.metadata.create_all(engine)

''' 
Add in extra scripts here to instantiate a database with 2 teams and 3 users per team with timesheets
'''
db = SessionLocal()

team_1 = models.Team(
    teamname="Team 1"
)

team_2 = models.Team(
    teamname="Team 2"
)

db.add(team_1)
db.add(team_2)

administrator = models.User(
    username="Administrator",
    hashed_password=hashFunc("admin"),
    hasAdmin=True,
    teamID=1
)
administrator_timesheet = models.Timesheet(
    owner=administrator,
)

john = models.User(
    username="John",
    hashed_password=hashFunc("doe"),
    hasAdmin=False,
    teamID=2
)
john_timesheet = models.Timesheet(
    owner=john,
)

teamLead = models.User(
    username="TeamLeader",
    hashed_password=hashFunc("scrum"),
    hasAdmin=True,
    teamID=2
)
teamLead_timesheet = models.Timesheet(
    owner=teamLead,
)

db.add(administrator)
db.add(administrator_timesheet)
db.add(john)
db.add(john_timesheet)
db.add(teamLead)
db.add(teamLead_timesheet)
db.commit()
