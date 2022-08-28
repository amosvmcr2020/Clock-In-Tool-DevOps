from database import Base, engine
from models import User, Team, Entry, Timesheet

print("Dropping existing database...")
Base.metadata.drop_all(engine)

print("Creating Database...")
Base.metadata.create_all(engine)

''' 
Add in extra scripts here to instantiate a database with 2 teams and 3 users per team with timesheets
'''
# db = SessionLocal()

# db.add()
