from database import Base, engine
from models import User, Team

print("Dropping existing database...")
Base.metadata.drop_all(engine)

print("Creating Database...")
Base.metadata.create_all(engine)