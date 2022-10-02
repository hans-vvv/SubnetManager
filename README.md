These demo scripts enable IPv4 subnet reservations for one or more IPv4 resource pools. For each resource pool reservations can be made only for a fixed prefix length. The data is stored in a Sqlite3 database and accessed using Python Sqlalchemy library.


Install with pip:
pip install fastapi "uvicorn[standard]" sqlalchemy

First run init_db.py script in order to put some demo data in the sqlite3 database.

Then run main.py and access the API documentation at
http://127.0.0.1:8001/docs

Then you could add a new pool of subnets using the appropriate POST method.

For example use this JSON data to provision a resource pool:

{
    "name": "10.7.0.0/24",
    "description": "test",
    "prefixlen": 29
}

The free subnets are returned by the app and can be viewed using the available GET methods.

The entered data is validated using the Python pydantic library at runtime. I also implemented a method in the IPv4SubnetManager class. The purpose of this class is to implement more complex logic which may be covererd completely by Pydantic. You could for example verify if a new subnetpool overlaps with the current available pools in the subnetpool_constraints method.

I used this great resource https://github.com/ChristopherGS/ultimate-fastapi-tutorial to implement certain features. The design patterns to implement database CRUD operations is worth exploring in detail.

Now a reservation can be made for a certain customer using this data 

{
    "status": "reserved",
    "cid": "customer1"
    "prefixlen_subnets": 29
}
 
on this URL:
http://127.0.0.1:8000/reserve_subnet

The first available free subnet will be allocated using the POST method.


Hans Verkerk, October 2022.