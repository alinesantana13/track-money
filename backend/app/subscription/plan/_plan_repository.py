from typing import Annotated

from fastapi import Depends
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.subscription.plan._plan import Plan


class PlanRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_plan_by_id(self, plan_id: int) -> Plan | None:
        return self.db.query(Plan).filter(Plan.id == plan_id).first()

    def get_plan_by_name(self, name: str) -> Plan | None:
        return self.db.query(Plan).filter(Plan.name == name).first()

    def list_plans(self) -> list[Plan]:
        return self.db.query(Plan).order_by(Plan.price.asc(), Plan.id.asc()).all()

    def create(self, plan: Plan) -> Plan:
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def create_if_missing(self, plan: Plan) -> None:
        statement = (
            insert(Plan)
            .values(
                name=plan.name,
                max_number_accounts=plan.max_number_accounts,
                price=plan.price,
                is_free=plan.is_free,
                created_at=plan.created_at,
            )
            .on_conflict_do_nothing(index_elements=["name"])
        )
        self.db.execute(statement)
        self.db.commit()


def get_plan_repository(db: Annotated[Session, Depends(get_db)]) -> PlanRepository:
    """
    Dependency injection for PlanRepository.
    """
    return PlanRepository(db)

PlanRepositoryDep = Annotated[PlanRepository, Depends(get_plan_repository)]