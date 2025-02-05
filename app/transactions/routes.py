from fastapi import APIRouter, Query

from app.db import SessionDep
from app.transactions.service import TransactionService

router = APIRouter()
service = TransactionService()

"""
@router.post('/transactions', status_code=status.HTTP_201_CREATED, tags=['Transactions'])
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer,transaction_data_dict.get('customer_id'))
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
        )
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

"""


@router.get("/transaction", tags=["Transactions"])
# GET TRANSACTIONS PAGINATE
# ----------------------
async def get_transactions_paginate(
    session: SessionDep,
    skip: int = Query(0, description="Registros a omitir"),
    limit: int = Query(10, description="Número de registros"),
):
    return service.get_transactions_paginate(session, skip, limit)
