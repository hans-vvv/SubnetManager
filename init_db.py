from sqlalchemy import create_engine

from app.db.models import Base

engine = create_engine("sqlite:///subnetmanager.db")
Base.metadata.drop_all(engine)
Base.metadata.create_all(bind=engine)

