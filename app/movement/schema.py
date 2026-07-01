from decimal import Decimal

from pydantic import BaseModel


class BankAccountCreate(BaseModel):
    name: str
    bank_name: str
    account_number: str
    initial_balance: Decimal = Decimal("0")


class BankAccountResponse(BaseModel):
    id: int
    name: str
    bank_name: str
    account_number: str
    balance: float
    status: str

    class Config:
        from_attributes = True
