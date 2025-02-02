from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from models import Plan, CustomerPlan
from db import SessionDep

router = APIRouter()

@router.post("/plans", tags=['Plans'])
def create_plan(plan_data:Plan, session: SessionDep):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db

@router.get("/plans", tags=['Plans'])
def list_plan(session: SessionDep):
    plans = session.exec(select(Plan)).all()
    return plans