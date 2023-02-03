from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings

engine = create_engine(
    settings.db_url, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
