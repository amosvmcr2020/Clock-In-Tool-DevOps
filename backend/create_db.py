from app.database import Base, engine
from app import models
from app.database import SessionLocal
import hashlib


def create_new_db():
    def hashFunc(password):
        return hashlib.sha256(password.encode("UTF-8")).hexdigest()

    print("Dropping existing database...")
    Base.metadata.drop_all(engine)

    print("Creating Database...")
    Base.metadata.create_all(engine)

    """ 
    Add in extra scripts here to instantiate a database with 2 teams and 3 users per team with timesheets
    """
    db = SessionLocal()

    team_1 = models.Team(teamname="Team 1")

    team_2 = models.Team(teamname="Team 2")

    db.add(team_1)
    db.add(team_2)

    administrator = models.User(
        username="Administrator",
        hashed_password=hashFunc("admin"),
        hasAdmin=True,
        teamID=1,
    )
    administrator_timesheet = models.Timesheet(
        owner=administrator,
    )

    john = models.User(
        username="John", hashed_password=hashFunc("doe"), hasAdmin=False, teamID=2
    )
    john_timesheet = models.Timesheet(
        owner=john,
    )

    teamLead = models.User(
        username="TeamLeader",
        hashed_password=hashFunc("scrum"),
        hasAdmin=True,
        teamID=2,
    )
    teamLead_timesheet = models.Timesheet(
        owner=teamLead,
    )

    entry1 = models.Entry(
        date="01/01/2022",
        time_in="2022-01-01T09:30:00.0",
        time_out="2022-01-01T17:00:00.0",
        timesheetID=1,
    )

    entry2 = models.Entry(
        date="01/02/2022",
        time_in="2022-01-02T09:30:00.0",
        time_out="2022-01-02T17:30:00.0",
        timesheetID=1,
    )

    entry3 = models.Entry(
        date="01/03/2022",
        time_in="2022-01-03T09:30:00.0",
        time_out="2022-01-03T16:30:00.0",
        timesheetID=1,
    )

    db.add(entry1)
    db.add(entry2)
    db.add(entry3)

    db.add(administrator)
    db.add(administrator_timesheet)
    db.add(john)
    db.add(john_timesheet)
    db.add(teamLead)
    db.add(teamLead_timesheet)
    db.commit()


create_new_db()
