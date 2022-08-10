from database import Base
from sqlalchemy import String, Boolean, Integer, Column, Text, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    username = Column(String(255), nullable = False, unique = True)
    hasAdmin = Column(Boolean, default = False)
    teamID = Column(Integer, ForeignKey("teams.id"), nullable=False)

    team = relationship("Team", back_populates="users")

    def __repr__(self):
        return f"{self.id} : {self.username} is an Admin" if self.hasAdmin else f"{id} : {self.username} is not an Admin"

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key = True)
    teamname = Column(String(255), nullable=False, unique = True)

    users = relationship("User", back_populates="team")

    def __repr__(self):
        return self.teamname