from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.db.models import SubnetPool
from app.schemas.schemas import SubnetPoolCreateBase, SubnetPoolCreateBase, SubnetPoolUpdateBase


class CRUDSubnetPool(CRUDBase[SubnetPool, SubnetPoolCreateBase, SubnetPoolUpdateBase]):
    
    def get_subnetpools_by_prefixlen(self, db: Session, pool_prefixlen: int
    )-> List[SubnetPool]:
        return db.query(SubnetPool).filter(SubnetPool.prefix_len_subnets == pool_prefixlen).all()

    def get_subnetpool_names(self, db: Session) -> List[dict]:
        return db.query(SubnetPool.prefixname).all()


subnetpool = CRUDSubnetPool(SubnetPool)
