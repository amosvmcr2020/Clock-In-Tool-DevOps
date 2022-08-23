from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


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
    id: Optional[int]
    date: Optional[str]

    time_in: Optional[datetime]
    time_out: Optional[datetime]

    timesheetID: int

    class Config:
        orm_mode = True


class Clock_req(BaseModel):
    millis_in: Optional[int]
    millis_out: Optional[int]
    timesheetID: int


class Timesheet(BaseModel):
    id: Optional[int]
    owner: User
    times: Optional[List[Entry]]

    class Config:
        orm_mode = True
