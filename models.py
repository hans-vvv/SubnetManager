import uuid
from typing import Optional, List, Union, Dict, Any
from pydantic import BaseModel, Field


class ReservationModel(BaseModel):

    cid: str
    prefixlen: int

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "cid": "Klant-1",
                "subnet": "10.24.0.0/29",                
            }
        }

    
class SubnetModel(BaseModel):
    
    name: str = Field(...)
    status: str = Field(...)
    cid: Union[str, None] = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "10.24.0.0/24",
                "status": "free",
                "cid": None,
            }
        }
  

class PoolModel(BaseModel):

    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    description: str = Field(...)
    prefixlen: int = Field(...)
    subnets: list[SubnetModel] = Field(default_factory=list)

    class Config:
        allow_population_by_field_name = True

##        schema_extra = {
##            "example": {
##                "name": "Jane Doe",
##                "description": "jdoe@example.com",
##            }
##        }


# print(PoolModel.schema_json(indent=2))
    


    

    
