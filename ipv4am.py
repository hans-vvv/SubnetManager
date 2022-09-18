import requests
import ipaddress

from typing import List, Dict
from collections import defaultdict


class IPv4SubnetManager:
    

    def _read_collection(self) -> None:

        self._pools = requests.get("http://127.0.0.1:8000/pools").json()
        
        # create lookup objects by iteration through all pools
        self._free_subnets = defaultdict(lambda: defaultdict(list)) # prefixlen, poolname -> [name of free subnet]
        self._poolnames = []
                
        for pool in self._pools:
            prefixlen = pool["prefixlen"]
            poolname = pool["name"]
            subnets = pool["subnets"]
            
            self._poolnames.append(poolname)
            
            for subnet in pool["subnets"]:
                
                if subnet["status"] == "Free":
                    self._free_subnets[prefixlen][poolname].append(subnet["name"])


    def check_pool_constraints(self, poolname, prefixlength):

        self._read_collection()

        if poolname in self._poolnames:
            raise ValueError("Duplicate Poolname")
       
 
    def create_free_subnets(self, poolname: str, subnet_prefixlen: int) -> List[Dict]:

        free_subnets = []
        
        pool_network = ipaddress.ip_network(poolname)
        pool_mask = str(ipaddress.IPv4Network(poolname).netmask)

        pool_prefixlen = bin(int(ipaddress.IPv4Address(pool_mask))).count("1")
        subnets = list(pool_network.subnets(prefixlen_diff=subnet_prefixlen-pool_prefixlen))
        subnets = [str(subnet) for subnet in subnets]

        return [{"name": subnet, "status": "Free", "cid": None} for subnet in subnets]
              

    def reserve_subnet(self, prefixlen: int, cid: str) -> str:

        self._read_collection()

        for poolname in self._free_subnets[prefixlen]:
            for first_free_subnet in self._free_subnets[prefixlen][poolname]:
                break
            
        old_subnet_info = {"name": first_free_subnet, "status": "Free", "cid": None}
        new_subnet_info = {"name": first_free_subnet, "status": "reserved", "cid": cid}

        for pool in self._pools:
            if poolname != pool["name"]:
                continue
            for i in range(len(pool["subnets"])):
                if pool["subnets"][i] == old_subnet_info:
                    pool["subnets"].pop(i)
                    pool["subnets"].insert(i, new_subnet_info)
                    break
        return pool["name"], pool["subnets"] 
