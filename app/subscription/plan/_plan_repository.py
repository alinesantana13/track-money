from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.subscription.plan._plan import Plan


class PlanRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_plan_by_id(self, plan_id):
        return self.db.query(Plan).filter(Plan.id == plan_id).first()


def get_plan_repository(db: Annotated[Session, Depends(get_db)]) -> PlanRepository:
    """
    Dependency injection for PlanRepository.
    """
    return PlanRepository(db)

PlanRepositoryDep = Annotated[PlanRepository, Depends(get_plan_repository)]