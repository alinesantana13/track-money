from app.movement.bank._bank_account import BankAccount
from app.movement.bank._bank_account_repository import BankAccountRepository


def list_bank_accounts(
    email: str,
    bank_account_repository: BankAccountRepository,
) -> list[BankAccount]:
    return bank_account_repository.get_all_by_user(email)
