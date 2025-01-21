from sqlmodel import select
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from db import SessionDep
from app import routers

from models import *

router = APIRouter()

@router.post("/customers",response_model=Customer,tags=['customers'])
async def create_customer(customer_data: CustomerCreate, session: SessionDep): 
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get("/customers/{customer_id}",response_model=Customer,tags=['customers'])
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=404,detail= "Customer doesn't exist")
    return customer_db

@router.delete("/customers/{customer_id}",response_model=Customer,tags=['customers'])
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=404,detail= "Customer doesn't exist")
    session.delete(customer_db)
    session.commit()
    return {"detail":"ok"}

@router.patch("/customers/{customer_id}",response_model=Customer,status_code=201,tags=['customers'] )
async def update_customer(customer_id: int,customer_data:CustomerCreate, session: SessionDep):
    #validacion de que el usuario existe
    customer_db = session.get(Customer, customer_id)
    
    if not customer_db:
        raise HTTPException(status_code=404,detail= "Customer doesn't exist")
    update_data = customer_data.model_dump(exclude_unset=True)
    
    try:
        Customer.model_validate(update_data)
    except ValidationError as e:
        raise HTTPException(status_code = 422,detail=str(e))
    
    customer_db.sqlmodel_update(update_data)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db
"""
@app.put("/customers/{customer_id}",response_model=Customer)
async def update_customer(customer_id: int,customer_data:CustomerCreate, session: SessionDep):
    #validacion de que el usuario existe
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=404,detail= "Customer doesn't exist")
    
    update_data = customer_data.model_dump(exclude_unset=True)
    
    #validacion de que los datos ingresados sean correctos
    try:
        Customer.model_validate(update_data)
    except ValidationError as e:
        raise HTTPException(status_code = 422,detail=str(e))
    
    for key,value in update_data.items():
        #esta funcion permite actualizar los datos como un diccionario
        setattr(customer_db,key,value)
    
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db"""

@router.get("/customers",response_model=list[Customer],tags=['customers'])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()
