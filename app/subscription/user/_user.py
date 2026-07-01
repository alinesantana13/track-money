from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.domain_error import DomainError
from app.infra.database import Base
from app.subscription.plan._plan import Plan
from app.subscription.user._user_plan import UserPlan


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "subscription"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    user_plans = relationship("UserPlan", back_populates="user")

    def __init__(self, name: str, email: str):
        DomainError.validate(
            name is not None and len(name) <= 128,
            "Name must be a non-empty string and at most 128 characters long.",
        )
        DomainError.validate(
            email is not None and len(email) <= 128,
            "Email must be a non-empty string and at most 128 characters long.",
        )
        
        self.name = name
        self.email = email
    
    def add_plan(self, plan: Plan):
        DomainError.validate(
            plan is not None, "Plan must be provided."
        )

        self._deactive_plans()
        user_plan = UserPlan(plan_id=plan.id, active=True)
        self.user_plans.append(user_plan)

    def _deactive_plans(self):
        for user_plan in self.user_plans:
            user_plan.active = False

    def get_active_plan(self) -> Plan | None:
        active_user_plan = next((up for up in self.user_plans if up.active), None)
        return active_user_plan.plan if active_user_plan else None
    