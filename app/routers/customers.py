from fastapi import APIRouter, HTTPException, Query, status
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

router = APIRouter()

# Create
#----------------------
@router.post(
        '/customers', response_model=Customer,
        status_code=status.HTTP_201_CREATED,
        tags=['Customers']
)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer
# GET ONE
#----------------------
@router.get('/customers/{customer_id}', response_model=Customer, tags=['Customers'])
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
        )
    return customer_db
# Update
#----------------------
@router.patch('/customers/{customer_id}', response_model=Customer, status_code=status.HTTP_201_CREATED, tags=['Customers'])
async def update_customer(customer_id: int, customer_data: CustomerUpdate , session: SessionDep):
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
# Delete
#----------------------
@router.delete('/customers/{customer_id}', tags=['Customers'])
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits")
    
    session.delete(customer_db)
    session.commit()
    return {"detail": "ok"}
# List All
#----------------------
@router.get('/customers', response_model= list[Customer], tags=['Customers'])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()
# Create - Customer Plans
#----------------------
@router.post("/customers/{customer_id}/plans/{plan_id}", tags=['Customers'])
async def subscribe_customer_to_plan(
    customer_id: int, plan_id:int, session: SessionDep, plan_status: StatusEnum = Query()
    ):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)

    if not customer_db or not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer or Plan doesn't exits"
        )
    customer_plan_db = CustomerPlan(
        plan_id=plan_db.id,customer_id=customer_db.id, status=plan_status
    )
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db
# List All - Customer Plans
#----------------------
@router.get("/customers/{customer_id}/plans", tags=['Customers'])
async def subscribe_customer_to_plan(
    customer_id: int, session: SessionDep, plan_status:StatusEnum = Query()
):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
        )
    query = (
        select(CustomerPlan)
        .where(CustomerPlan.customer_id==customer_id)
        .where(CustomerPlan.status==plan_status)
    )
    plans = session.exec(query).all()
    return plans
# Create - Customer Transactions
#----------------------
@router.post("/customers/{customer_id}/transactions",response_model=Transaction,tags=['Customers'])
async def create_customer_transaction(customer_id:int, transaction_data: TransactionCreate, session:SessionDep):
    customer_db = session.get(Customer,customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doen't exits"
        )
    customer_transaction_data_dict = transaction_data.model_dump(exclude_unset=True)
    customer_transaction_data_dict['customer_id'] = customer_id

    transaction_db = Transaction.model_validate(customer_transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db
# List All - Customer Transactions
#----------------------
@router.get('/customer/{customer_id}/transactions',tags=['Customers'])
async def list_customer_transaction(customer_id:int, session:SessionDep):
    customer_db = session.get(Customer,customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doen't exits"
        )
    
    query = select(Transaction).where(Transaction.customer_id==customer_id)
    transactions_list = session.exec(query).all()
    return transactions_list