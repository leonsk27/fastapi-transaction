from fastapi import APIRouter, Query, status, HTTPException
from sqlmodel import select
from app.models import Plan, PlanCreate, PlanUpdate
from app.db import SessionDep

router = APIRouter()
# Create
#----------------------
@router.post("/plans",response_model=Plan, tags=['Plans'])
def create_plan(plan_data:PlanCreate, session: SessionDep):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db
# GET ONE
#----------------------
@router.get('/plans/{plan_id}',response_model=Plan, tags=["Plans"])
async def read_plan(plan_id:int, session:SessionDep):
    plan_db = session.get(Plan,plan_id)
    if not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan doesn't exits"
        )
    return plan_db

# Update
#----------------------
@router.patch('/plans/{plan_id}',response_model=Plan, status_code=status.HTTP_201_CREATED, tags=['Plans'])
async def update_plan(plan_id: int, plan_data: PlanUpdate, session: SessionDep):
    plan_db = session.get(Plan,plan_id)
    if not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail = "Plan doesn't exits"
        )
    plan_data_dict = plan_data.model_dump(exclude_unset=True)
    plan_db.sqlmodel_update(plan_data_dict)
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db
# List All
#----------------------
@router.get('/plans',response_model=list[Plan],  tags=['Plans'])
def list_plan(session: SessionDep):
    return session.exec(select(Plan)).all()
# Delete
#----------------------
@router.delete('/plans/{plan_id}',tags=["Plans"])
def delete_plan(plan_id:int, session: SessionDep):
    plan_db =  session.get(Plan,plan_id)
    if not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan doesn't exits"
        )
    session.delete(plan_db)
    session.commit()
    return {'detail':'ok'}