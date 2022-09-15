These demo scripts enable IP subnet reservations from one or more IPv4 resource pools. For each resource pool reservations can be made only for a fixed prefix length. The data containing the pools and reservations is dumped on disk using JSON serilization.

Install with pip:

pip install fastapi "uvicorn[standard]"

Start webserver via console with:
uvicorn main:app --reload

A resouce pool can be provisioned via REST API (Postman) with this URL:

http://127.0.0.1:8000/api/v1/pools

Use this JSON data in raw body and POST this data:

{
    "name": "10.4.0.0/24",
    "description": "test",
    "prefixlen": 29,
    "subnets": []
 }


The data can be viewed using GET method on the same URL.

Now a reservation can be made for a certain customer using this data 

{
    "cid": "klant-1",
    "prefixlen": 29
}
 
on this URL:

http://127.0.0.1:8000/api/v1/reserve_subnet


The text file can opened to verify that a subnet has been reserved for the customer.


Hans Verkerk, Sept 2022.






















