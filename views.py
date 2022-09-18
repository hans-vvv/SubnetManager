import requests
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from ipv4am import IPv4SubnetManager
from typing import List

from models import PoolModel, ReservationModel

router = APIRouter()

ism = IPv4SubnetManager()


@router.get("/pools", response_description="List all pools")
def read_pools(request: Request) -> List[PoolModel]:
    return list(request.app.database["pools"].find(limit=100))

@router.post("/pools", response_description="Add new pool", response_model=PoolModel)
def create_pool(request: Request, pool: PoolModel = Body(...)):
    pool = jsonable_encoder(pool)
    ism.check_pool_constraints(pool["name"], pool["prefixlen"])
    free_subnets = ism.create_free_subnets(pool["name"], pool["prefixlen"])
    pool.update({"subnets": free_subnets})
    new_pool = request.app.database["pools"].insert_one(pool)
    created_pool = request.app.database["pools"].find_one({"_id": new_pool.inserted_id}) 
    return created_pool

@router.post("/reserve_subnet")
def reserve_subnet(request: Request, reservation: ReservationModel = Body(...)):
    reservation = jsonable_encoder(reservation)
    cid = reservation["cid"]
    prefixlen = reservation["prefixlen"]
    poolname, new_subnets = ism.reserve_subnet(prefixlen, cid)
    request.app.database["pools"].update_one({"name": poolname}, { "$set": { "subnets": new_subnets }})          
    return new_subnets


    
    
    
    






    

    






    
