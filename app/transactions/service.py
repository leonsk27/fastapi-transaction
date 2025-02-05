from sqlmodel import select

from app.db import SessionDep
from app.models import Transaction


class TransactionService:
    # GET TRANSACTIONS PAGINATE
    # ----------------------
    def get_transactions_paginate(
        self,
        session: SessionDep,
        skip: int,
        limit: int,
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
