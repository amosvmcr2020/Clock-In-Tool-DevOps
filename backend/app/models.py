from . import database
from sqlalchemy import String, Boolean, Integer, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class User(database.Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    hasAdmin = Column(Boolean, default=False)
    teamID = Column(Integer, ForeignKey("teams.id"), nullable=False)
    timesheetID = Column(Integer, ForeignKey("timesheets.id"), nullable=False)

    timesheet = relationship("Timesheet", back_populates="owner", uselist=False)
    team = relationship("Team", back_populates="users", uselist=False)


class Team(database.Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    teamname = Column(String(255), nullable=False, unique=True)

    users = relationship("User", back_populates="team")


class Timesheet(database.Base):
    __tablename__ = "timesheets"
    id = Column(Integer, primary_key=True)

    owner = relationship("User", back_populates="timesheet", uselist=False)
    times = relationship("Entry", back_populates="timesheet")


class Entry(database.Base):
    __tablename__ = "time_entries"
    id = Column(Integer, primary_key=True)

    date = Column(String, nullable=False)

    time_in = Column(DateTime, nullable=False)
    time_out = Column(DateTime, nullable=True)
    timesheetID = Column(Integer, ForeignKey("timesheets.id"), nullable=False)

    timesheet = relationship("Timesheet", back_populates="times", uselist=False)
