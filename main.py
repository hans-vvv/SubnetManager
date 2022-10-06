from fastapi import FastAPI, Request, HTTPException
from fastapi.encoders import jsonable_encoder

from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError

from sqlite3 import Connection as SQLite3Connection

from app import crud
from app import subnet_logic
from app.core.config import settings
from app.db.session import SessionLocal

from app.db.models import SubnetPool
from app.schemas.schemas import SubnetPoolCreateBase, SubnetUpdateBase
    

app = FastAPI()
db = SessionLocal()


# Enable sqlite3 referential integrity checks
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


@app.get("/subnetpool")
def get_subnetpools():   
    return crud.subnetpool.get_multi(db)

@app.get("/subnetpool/{item_id}")
def get_pool(item_id: int):
    return crud.subnetpool.get(db, item_id)

@app.get("/subnet")
def get_subnets():
    return crud.subnet.get_multi(db)

@app.get("/subnet/{item_id}")
def get_subnet(item_id: int):
    return crud.subnet.get(db, item_id)

@app.get("/subnets_by_subnetpool_id/{item_id}")
def get_subnets_by_subnetpool_id(item_id: int):
    return crud.subnet.get_subnets_by_subnetpool_id(db, item_id)

@app.get("/free_subnet_by_prefixlen/{prefixlen}")
def get_free_subnet_by_prefixlen(prefixlen: int):
    return crud.subnet.get_free_subnet_by_prefixlen(db, prefixlen)

@app.get("/subnetpool_names")
def get_subnetpool_names():
    return crud.subnetpool.get_subnetpool_names(db)

@app.post("/subnetpool")
def create_subnetpool(obj_in: SubnetPoolCreateBase):
    result, detail = subnet_logic.ipv4subnetmanager.subnetpool_constraints(obj_in)
    if result == False:
        raise HTTPException(
            status_code=403, detail=detail
        )
    try:
        created_subnetpool = crud.subnetpool.create(db, obj_in=obj_in)        
        return subnet_logic.ipv4subnetmanager.create_free_subnets(db, created_subnetpool)
    except IntegrityError:
        raise HTTPException(
            status_code=403, detail="Something went wrong when adding this pool in the db."
        )

@app.post("/reserve_subnet")
def reserve_subnet(obj_in: SubnetUpdateBase):
    try:
        obj_in_data = jsonable_encoder(obj_in)
        prefixlen_subnets = obj_in_data['prefixlen_subnets']
        free_subnet = crud.subnet.get_free_subnet_by_prefixlen(db, prefixlen_subnets)
        return crud.subnet.update(db, db_obj=free_subnet, obj_in=obj_in)
    except TypeError:
        raise HTTPException(
            status_code=403, detail="No free IPv4 resources available."
        )


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
