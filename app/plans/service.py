from fastapi import HTTPException, status
from sqlmodel import select

from app.db import SessionDep
from app.models import Plan, PlanCreate, PlanUpdate


class PlanService:
    # CREATE
    # ----------------------
    def create_plan(self, plan_data: PlanCreate, session: SessionDep):
        plan_db = Plan.model_validate(plan_data.model_dump())
        session.add(plan_db)
        session.commit()
        session.refresh(plan_db)
        return plan_db

    # GET ONE
    # ----------------------
    def read_plan(self, plan_id: int, session: SessionDep):
        plan_db = session.get(Plan, plan_id)
        if not plan_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Plan doesn't exits"
            )
        return plan_db

    # UPDATE
    # ----------------------
    def update_plan(self, plan_id: int, plan_data: PlanUpdate, session: SessionDep):
        plan_db = session.get(Plan, plan_id)
        if not plan_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Plan doesn't exits"
            )
        plan_data_dict = plan_data.model_dump(exclude_unset=True)
        plan_db.sqlmodel_update(plan_data_dict)
        session.add(plan_db)
        session.commit()
        session.refresh(plan_db)
        return plan_db

    # GET ALL PLANS
    # ----------------------
    def get_all_plans(self, session: SessionDep):
        return session.exec(select(Plan)).all()

    # DELETE
    # ----------------------
    def delete_plan(self, plan_id: int, session: SessionDep):
        plan_db = session.get(Plan, plan_id)
        if not plan_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Plan doesn't exits"
            )
        session.delete(plan_db)
        session.commit()
        return {"detail": "ok"}
