from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env="DATABASE_URL")
    # In order to run the tests locally, please have a local postgres server running and uncomment the following line:
    # db_url: str = "postgresql://postgres:password@localhost/Timesheet"


settings = Settings()
