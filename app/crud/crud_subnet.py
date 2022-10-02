from typing import List, Optional

from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.db.models import Subnet, SubnetPool
from app.schemas.schemas import SubnetCreateBase, SubnetUpdateBase


class CRUDSubnet(CRUDBase[Subnet, SubnetCreateBase, SubnetUpdateBase]):

    def get_subnets_by_subnetpool_id(self, db: Session, id: int
    )-> List[Subnet]:
        return db.query(Subnet).filter(Subnet.subnetpool_id == id).all()

    def get_free_subnet_by_prefixlen(self, db: Session, prefixlen: int
    )-> Subnet:
        record = db.query(
            Subnet
            ) \
            .join(SubnetPool) \
            .filter(SubnetPool.prefixlen_subnets == prefixlen) \
            .filter(Subnet.status == "free") \
            .first()                 
        return record
        
subnet = CRUDSubnet(Subnet)
