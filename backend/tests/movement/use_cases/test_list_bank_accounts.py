from decimal import Decimal

from app.movement.bank._bank_account import AccountStatus, BankAccount, User
from app.movement.use_cases.list_bank_accounts import list_bank_accounts


class StubBankAccountRepository:
    def __init__(self, accounts: list[BankAccount]):
        self.accounts = accounts
        self.requested_email = None

    def get_all_by_user(self, user_email: str) -> list[BankAccount]:
        self.requested_email = user_email
        return self.accounts


def build_account() -> BankAccount:
    return BankAccount(
        name="Primary",
        bank_name="NuBank",
        account_number="ACC123",
        user=User(name="Aline", email="aline@example.com"),
        balance=Decimal("150.00"),
    )


def test_list_bank_accounts_returns_accounts_for_authenticated_user():
    accounts = [build_account()]
    repository = StubBankAccountRepository(accounts)

    result = list_bank_accounts("aline@example.com", repository)

    assert result == accounts
    assert repository.requested_email == "aline@example.com"
    assert result[0].status == AccountStatus.ACTIVE.value
