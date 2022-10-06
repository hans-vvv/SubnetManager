import ipaddress
from typing import List, Dict, Tuple

from fastapi.encoders import jsonable_encoder

import app.crud
from app.db.models import SubnetPool
from app.schemas.schemas import SubnetPoolCreateBase

from sqlalchemy.orm import Session


class IPv4SubnetManager:
    
    def subnetpool_constraints(self, obj_in: SubnetPoolCreateBase
    ) -> Tuple[bool, str]:

        obj_in_data = jsonable_encoder(obj_in)
        subnetpoolname = obj_in_data['prefixname']
        prefixlen_subnets = obj_in_data['prefixlen_subnets']

        try:
            pool_network = ipaddress.ip_network(subnetpoolname)
        except ValueError:
            detail = 'Invalid IPv4 network'
            return False, detail
        return True, ''        
 
    def create_free_subnets(self, db: Session, subnetpool: SubnetPool
    ) -> List[Dict]:

        subnetpool_id = db.query(subnetpool.id).first()[0]
        subnetpool_dict = jsonable_encoder(subnetpool)
        subnetpoolname = subnetpool_dict['prefixname']
        prefixlen_subnets = subnetpool_dict['prefixlen_subnets']
       
        pool_network = ipaddress.ip_network(subnetpoolname)
        pool_mask = str(ipaddress.IPv4Network(subnetpoolname).netmask)
        pool_prefixlen = bin(int(ipaddress.IPv4Address(pool_mask))).count("1")
        subnets = list(pool_network.subnets(prefixlen_diff=prefixlen_subnets-pool_prefixlen))

        subnet_names = [str(subnet) for subnet in subnets]
        free_subnets = [{'prefixname': subnet_name, 'status': 'free', 'cid': '', 'subnetpool_id': subnetpool_id}
                        for subnet_name in subnet_names]
        # Create objects in db
        for free_subnet in free_subnets:
            app.crud.subnet.create(db, obj_in=free_subnet)
        return free_subnets           
 
 
ipv4subnetmanager = IPv4SubnetManager()
