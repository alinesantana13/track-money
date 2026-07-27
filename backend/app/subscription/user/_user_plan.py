import pendulum
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.domain_error import DomainError
from app.infra.database import Base
from app.subscription.plan._plan import Plan


class UserPlan(Base):
    __tablename__ = "user_plans"
    __table_args__ = {"schema": "subscription"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("subscription.users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("subscription.plans.id"), nullable=False)
    active = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False)

    user = relationship("app.subscription.user._user.User", back_populates="user_plans")
    plan = relationship(Plan)

    def __init__(self, plan_id: int, active: bool = False):
        DomainError.validate(
            plan_id is not None and plan_id > 0, "Plan ID must be a positive integer."
        )
        self.plan_id = plan_id
        self.active = active
        self.created_at = pendulum.now("UTC")