from decimal import Decimal
from enum import Enum

from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.orm import composite

from app.core.domain_error import DomainError
from app.infra.database import Base


class AccountStatus(Enum):
    """Enumeration for the status of a bank account."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    CLOSED = "closed"
    SUSPENDED = "suspended"


class User:
    name: str
    email: str


    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

        DomainError.validate(
            name and len(name) <= 128, "Name must be at most 128 characters long."
        )

        DomainError.validate(
            email and "@" in email and len(email) <= 128,
            "Email must be a non-empty string with a maximum length of 128 characters."
        )

    def __composite_values__(self):
        """Required method for SQLAlchemy composite types."""
        return self.name, self.email


class BankAccount(Base):
    __tablename__ = "bank_account"
    __table_args__ = {"schema": "movement"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(24), nullable=False)
    bank_name = Column(String(24), nullable=False)
    account_number = Column(String(24), nullable=False)
    balance = Column(Numeric(precision=15, scale=2), nullable=False, default=0.0)
    status = Column(String(20), nullable=False, default=AccountStatus.ACTIVE.value)
    _user_name = Column("user_name", String(128), nullable=False)
    _user_email = Column("user_email", String(128), nullable=False)
    user = composite(User, _user_name, _user_email)

    def __init__(
        self,
        name: str,
        bank_name: str,
        account_number: str,
        user: User,
        balance: Decimal = Decimal(0)
    ):
        DomainError.validate(
            name and len(name) <= 24, "Name must be at most 24 characters long."
        )
        DomainError.validate(
            bank_name and len(bank_name) <= 24,
            "Bank name must be at most 24 characters long."
        )
        DomainError.validate(
            account_number and len(account_number) <= 24,
            "Account number must be at most 24 characters long."
        )
        DomainError.validate(
            balance is not None and balance >= 0,
            "Balance must be a non-negative decimal number."
        )

        self.name = name
        self.bank_name = bank_name
        self.account_number = account_number
        self.user = user
        self.balance = balance
        self.status = AccountStatus.ACTIVE.value

