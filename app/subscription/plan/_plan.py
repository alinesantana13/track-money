import pendulum
from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.core.domain_error import DomainError
from app.infra.database import Base


# Plan Free: 1 account, Plan Premium: 5 accounts, Plan Enterprise: 10 accounts
class Plan(Base):
    __tablename__ = "plans"
    __table_args__ = {"schema": "subscription"}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(24), unique=True, index=True, nullable=False)
    max_number_accounts = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)  # Price in cents
    is_free = Column(Boolean, nullable=False, default=False )  # 1 for free, 0 for paid
    created_at = Column(DateTime, nullable=False)

    def __init__(
        self,
        name: str,
        max_number_accounts: int,
        price: int
    ):
        DomainError.validate(
            name and len(name) <= 24,
            "Plan name must be a non-empty string with a maximum length of 24 characters."
        )
        DomainError.validate(
            max_number_accounts >= 0,
            "Max number of accounts must be a non-negative integer."
        )
        self.name = name
        self.max_number_accounts = max_number_accounts
        self.price = price
        self.is_free = False
        if price == 0:
            self.is_free = True
        self.created_at = pendulum.now("UTC")