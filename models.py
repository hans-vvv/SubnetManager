from typing import Optional, List
from pydantic import BaseModel


class Reservation(BaseModel):

    cid: str
    prefixlen: int


class Subnet(BaseModel):

    name: str
    status: str
    cid: str
    

class Pool(BaseModel):

    name: str
    description: str
    prefixlen: int
    subnets: List[Subnet]
    


    

    
