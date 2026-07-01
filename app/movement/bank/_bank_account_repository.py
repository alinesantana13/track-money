from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.movement.bank._bank_account import BankAccount


class BankAccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, bank_account: BankAccount):
        self.db.add(bank_account)
        self.db.commit()
        self.db.refresh(bank_account)

    def count_by_user(self, user_email: str) -> int:
        return (
            self.db.query(BankAccount)
            .filter(BankAccount._user_email == user_email)
            .count()
        )

    def get_all_by_user(self, user_email: str) -> list[BankAccount]:
        return (
            self.db.query(BankAccount)
            .filter(BankAccount._user_email == user_email)
            .all()
        )

def get_bank_account_repository(
    db: Annotated[Session, Depends(get_db)],
) -> BankAccountRepository:
    return BankAccountRepository(db)


BankAccountRepositoryDep = Annotated[
    BankAccountRepository, Depends(get_bank_account_repository)
]