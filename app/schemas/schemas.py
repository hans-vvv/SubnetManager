from typing import List
from pydantic import BaseModel


#### Subnet definitions

class SubnetBase(BaseModel):
    prefixname: str
    status: str
    cid: str

 
class SubnetCreateBase(BaseModel):
    prefixname: str
    status: str
    cid: str
    subnetpool_id: int
    
  
class SubnetUpdateBase(BaseModel):
    status: str
    cid: str
    prefixlen_subnets: int


#### SubnetPool definitions

class SubnetPoolBase(BaseModel):
    prefixname: str
    description: str
    prefixlen_subnets: int


class SubnetPoolCreateBase(BaseModel):
    prefixname: str
    description: str
    prefixlen_subnets: int


class SubnetPoolUpdateBase(BaseModel):
    ...
