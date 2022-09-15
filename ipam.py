import json
import ipaddress
from collections import defaultdict


class SubnetIpManager:
    

    def __init__(self):
        
        #self._read_data_from_disk()
        self.data = []
      

    def read_data_from_disk(self):

        with open('subnet_ippam_data.txt') as f:
            self.data = json.load(f)

        # Create lookup tables (queries)
        self.free_subnets = defaultdict(lambda: defaultdict(list))

        for pool in self.data:
            prefixlen = pool["prefixlen"]
            poolname = pool["name"]
            for subnet in pool["subnets"]:
                if subnet["status"] == "free":
                    self.free_subnets[prefixlen][poolname].append(subnet["name"])

                    
    def write_data_to_disk(self):

        with open('subnet_ippam_data.txt', 'w') as f:
            json.dump(self.data, f, indent=4)
        
 
    def create_free_subnets(self, poolname, prefixlen):

        free_subnets = []
        
        pool_network = ipaddress.ip_network(poolname)
        pool_mask = str(ipaddress.IPv4Network(poolname).netmask)

        subnet_prefixlen = prefixlen
        pool_prefixlen = bin(int(ipaddress.IPv4Address(pool_mask))).count("1")
        subnets = list(pool_network.subnets(prefixlen_diff=subnet_prefixlen-pool_prefixlen))
        subnets = [str(subnet) for subnet in subnets]

        for subnet in subnets:
            free_subnets.append({"name": subnet, 'status': 'free', 'cid': None})
        return free_subnets
              

    def reserve_subnet(self, prefixlen, cid):

        for poolname in self.free_subnets[prefixlen]:
            for first_free_subnet in self.free_subnets[prefixlen][poolname]:
                break
            
        old_subnet_info = {"name": first_free_subnet, "status": "free", "cid": None}
        new_subnet_info = {"name": first_free_subnet, "status": "reserved", "cid": cid}

        for pool in self.data:
            if poolname != pool["name"]:
                continue
            for i in range(len(pool["subnets"])):
                if pool["subnets"][i] == old_subnet_info:
                    pool["subnets"].pop(i)
                    pool["subnets"].insert(i, new_subnet_info)
                    break
        return first_free_subnet
    

    






    
