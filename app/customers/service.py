from fastapi import HTTPException, Query, status
from sqlmodel import select

from app.db import SessionDep
from app.models import (
    Customer,
    CustomerCreate,
    CustomerPlan,
    CustomerUpdate,
    Plan,
    StatusEnum,
    Transaction,
    TransactionCreate,
)


class CustomerService:
    # CREATE
    # ----------------------
    def create_customer(self, customer_data: CustomerCreate, session: SessionDep):
        try:
            customer = Customer.model_validate(customer_data.model_dump())
            session.add(customer)
            session.commit()
            session.refresh(customer)
            return customer
        except Exception:
            session.rollback
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server error, create customer",
            )

    # GET ONE
    # ----------------------
    def read_customer(self, customer_id: int, session: SessionDep):
        customer_db = session.get(Customer, customer_id)
        if not customer_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
            )
        return customer_db

    # UPDATE
    # ----------------------
    def update_customer(
        self, customer_id: int, customer_data: CustomerUpdate, session: SessionDep
    ):
        customer_db = session.get(Customer, customer_id)
        if not customer_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
            )
        customer_data_dict = customer_data.model_dump(exclude_unset=True)
        customer_db.sqlmodel_update(customer_data_dict)
        session.add(customer_db)
        session.commit()
        session.refresh(customer_db)
        return customer_db

    # DELETE
    # ----------------------
    def delete_customer(self, customer_id: int, session: SessionDep):
        customer_db = session.get(Customer, customer_id)
        if not customer_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
            )

        session.delete(customer_db)
        session.commit()
        return {"detail": "ok"}

    # GET ALL CUSTOMERS
    # ----------------------
    def get_all_customers(self, session: SessionDep):
        statement = select(Customer)
        res = session.exec(statement)
        return res.all()
        # return session.exec(select(Customer)).all()

    # CREATE - CUSTOMER PLAN
    # ----------------------

    def create_customer_plan(
        self,
        customer_id: int,
        plan_id: int,
        session: SessionDep,
        plan_status: StatusEnum = Query(),
    ):
        customer_db = session.get(Customer, customer_id)
        plan_db = session.get(Plan, plan_id)

        if not customer_db or not plan_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer or Plan doesn't exits",
            )
        customer_plan_db = CustomerPlan(
            plan_id=plan_db.id, customer_id=customer_db.id, status=plan_status
        )
        session.add(customer_plan_db)
        session.commit()
        session.refresh(customer_plan_db)
        return customer_plan_db

    #   LIST All - CUSTOMER PLANS
    # ----------------------
    def get_all_customer_plans(
        self, customer_id: int, session: SessionDep, plan_status: StatusEnum = Query()
    ):
        customer_db = session.get(Customer, customer_id)
        if not customer_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
            )
        query = (
            select(CustomerPlan)
            .where(CustomerPlan.customer_id == customer_id)
            .where(CustomerPlan.status == plan_status)
        )
        plans = session.exec(query).all()
        return plans

    # CREATE - CUSTOMER TRANSACTION
    # ----------------------
    def create_customer_transaction(
        self, customer_id: int, transaction_data: TransactionCreate, session: SessionDep
    ):
        customer_db = session.get(Customer, customer_id)
        if not customer_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Customer doen't exits"
            )
        customer_transaction_data_dict = transaction_data.model_dump(exclude_unset=True)
        customer_transaction_data_dict["customer_id"] = customer_id

        transaction_db = Transaction.model_validate(customer_transaction_data_dict)
        session.add(transaction_db)
        session.commit()
        session.refresh(transaction_db)
        return transaction_db

    # GET All CUSTOMER TRANSACTIONS
    # ----------------------
    def get_all_customer_transactions(self, customer_id: int, session: SessionDep):
        customer_db = session.get(Customer, customer_id)
        if not customer_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Customer doen't exits"
            )

        query = select(Transaction).where(Transaction.customer_id == customer_id)
        transactions_list = session.exec(query).all()
        return transactions_list
