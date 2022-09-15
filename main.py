from typing import List
from fastapi import FastAPI
from models import Pool, Reservation
from ipam import SubnetIpManager
from fastapi.encoders import jsonable_encoder


app = FastAPI()
sim = SubnetIpManager()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/pools")
async def get_data() -> List[Pool]:
    return sim.data


@app.post("/api/v1/pools")
async def add_pool(pool: Pool):
    pool = jsonable_encoder(pool)
    poolname = pool["name"]
    prefixlen = pool["prefixlen"]
    free_subnets = sim.create_free_subnets(poolname, prefixlen)
    pool.update({"subnets": free_subnets})
    sim.data.append(pool)
    sim.write_data_to_disk()
    return pool


@app.post("/api/v1/reserve_subnet")
async def reserve_subnet(reservation: Reservation) -> str:
    reservation = jsonable_encoder(reservation)
    cid = reservation["cid"]
    prefixlen = reservation["prefixlen"]
    sim.read_data_from_disk()
    reserved_subnet = sim.reserve_subnet(prefixlen, cid)
    sim.write_data_to_disk()
    return reserved_subnet
    
    
    
    






    

    






    
