from fastapi import APIRouter, status

from app.db import SessionDep
from app.models import Plan, PlanCreate, PlanUpdate
from app.plans.service import PlanService

router = APIRouter()
service = PlanService()


# CREATE
# ----------------------
@router.post("/", response_model=Plan)
async def create_plan(plan_data: PlanCreate, session: SessionDep):
    return service.create_plan(plan_data, session)


# GET ONE
# ----------------------
@router.get("/{plan_id}", response_model=Plan)
async def read_plan(plan_id: int, session: SessionDep):
    return service.read_plan(plan_id, session)


# UPDATE
# ----------------------
@router.patch("/{plan_id}", response_model=Plan, status_code=status.HTTP_201_CREATED)
async def update_plan(plan_id: int, plan_data: PlanUpdate, session: SessionDep):
    return service.update_plan(plan_id, plan_data, session)


# GET ALL PLANS
# ----------------------
@router.get("/", response_model=list[Plan])
async def get_all_plans(session: SessionDep):
    return service.get_all_plans(session)


# DELETE
# ----------------------
@router.delete("/{plan_id}")
def delete_plan(plan_id: int, session: SessionDep):
    return service.delete_plan(plan_id, session)
