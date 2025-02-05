from fastapi import APIRouter, Query
from sqlmodel import select

from app.db import SessionDep
from app.models import Transaction

router = APIRouter()

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
async def list_transaction(
    session: SessionDep,
    skip: int = Query(0, description="Registros a omitir"),
    limit: int = Query(10, description="Número de registros"),
):
    query = select(Transaction).offset(skip).limit(limit)
    transactions = session.exec(query).all()

    len_transations = len(session.exec(select(Transaction)).all())
    total_pages = len_transations // limit
    current_page = len(transactions)

    message = {
        "total_pages": total_pages,
        "current_page": current_page,
        "total_transactions": len_transations,
    }

    return {"transactions": transactions, "message": message}
