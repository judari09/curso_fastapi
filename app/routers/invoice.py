from models import *
from fastapi import APIRouter
router = APIRouter()

@router.post("/invoices",tags=['invoices'])
async def create_invoice(invoice_data: Invoice):
    return invoice_data

