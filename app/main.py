from email.policy import HTTP
import zoneinfo
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from models import *
from db import *
from sqlmodel import *
from .routers import customers,transactions,invoice,plans
    
app = FastAPI(lifespan=create_all_tables)

app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoice.router)
app.include_router(plans.router)

@app.get("/")
async def root():
    return {"message":"Hola mundo xd"}


country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}
@app.get("/time/{iso_code}")
async def time(iso_code:str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time":datetime.now(tz)}

db_customer: list[Customer] = []






