import zoneinfo
from datetime import datetime
from fastapi import FastAPI
from models import *
from db import *
from sqlmodel import *
    
app = FastAPI(lifespan=create_all_tables)

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

@app.post("/customers",response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.post("/Transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data

@app.get("/customers",response_model=list[Customer])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()

@app.get("/customersid/{id}")
async def list_customer(id:int):
    return db_customer[id]