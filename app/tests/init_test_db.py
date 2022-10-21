from sqlalchemy import create_engine

from app.db.models import Base

def create_test_db():

    engine = create_engine("sqlite:///testsubnetmanager.db")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)
