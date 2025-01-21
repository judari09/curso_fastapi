from sqlmodel import select
from pydantic import ValidationError
from models import *
from fastapi import APIRouter, HTTPException
from db import SessionDep

router = APIRouter()

@router.post("/transactions",tags=['transactions'])
async def create_transaction(transaction_data: TransactionCreate,session: SessionDep):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get('customer_id'))
    if not customer:
        raise HTTPException(status_code=404,detail= "Customer doesn't exist")
    
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

@router.get("/transactions/{transaction_id}",response_model=Transaction,tags=['transactions'])
async def read_transaction(transaction_id: int, session: SessionDep):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(status_code=404,detail= "Customer doesn't exist")
    return transaction_db

@router.patch("/transactions/{transaction_id}",response_model=Transaction,status_code=201,tags=['transactions'] )
async def update_transaction(transaction_id: int,customer_data:TransactionCreate, session: SessionDep):
    #validacion de que el usuario existe
    transaction_db = session.get(Transaction, transaction_id)
    
    if not transaction_db:
        raise HTTPException(status_code=404,detail= "Customer doesn't exist")
    update_data = customer_data.model_dump(exclude_unset=True)
    
    try:
        Customer.model_validate(update_data)
    except ValidationError as e:
        raise HTTPException(status_code = 422,detail=str(e))
    
    transaction_db.sqlmodel_update(update_data)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db
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


@router.delete("/transactions/{transaction_id}",response_model=Transaction,tags=['transactions'])
async def delete_transaction(transaction_id: int, session: SessionDep):
    transaction_db = session.get(Transaction, transaction_id)
    if not transaction_db:
        raise HTTPException(status_code=404,detail= "Customer doesn't exist")
    session.delete(transaction_db)
    session.commit()
    return {"detail":"ok"}



@router.get("/transactions",response_model=list[Transaction],tags=['transactions'])
async def list_transactions(session: SessionDep):
    return session.exec(select(Transaction)).all()