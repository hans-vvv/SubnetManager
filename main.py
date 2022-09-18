from fastapi import FastAPI
from views import router as pool_router
import pymongo


app = FastAPI()
app.mongodb_client = pymongo.MongoClient("localhost", 27017)
app.database = app.mongodb_client["ipv4subnetpools"]

app.include_router(pool_router, tags=["pools"])

    
    
    






    

    






    
