These demo scripts enable IPv4 subnet reservations from one or more IPv4 resource pools. For each resource pool reservations can be made only for a fixed prefix length. The data is stored on a Mongodb dB.


Install with pip:

pip install fastapi "uvicorn[standard]"
pip install pymongo

Start webserver via console with:
uvicorn main:app --reload

A resouce pool can be provisioned via REST API via this URL:

http://127.0.0.1:8000/pools

Use this JSON data to provision a resource pool:

{
    "name": "10.5.0.0/24",
    "description": "test",
    "prefixlen": 29
}


The data can be viewed using GET method on the same URL.

Now a reservation can be made for a certain customer using this data 

{
    "cid": "klant-1",
    "prefixlen": 29
}
 
on this URL:

http://127.0.0.1:8000/reserve_subnet


Hans Verkerk, Sept 2022.






















