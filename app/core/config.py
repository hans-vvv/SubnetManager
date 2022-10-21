import pathlib
from typing import Optional

from pydantic import BaseSettings


# Project root directory
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite:///subnetmanager.db"
    SQLALCHEMY_TEST_DATABASE_URI: Optional[str] = "sqlite:///testsubnetmanager.db"
    

settings = Settings()
