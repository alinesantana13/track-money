from dataclasses import dataclass
from decimal import Decimal

import pytest

from app.movement.schema import BankAccountCreate
from app.movement.use_cases.register_bank_account import (
    AccountLimitReachedError,
    NoActivePlanError,
    UserNotFoundError,
    register_bank_account,
)


@dataclass
class FakeUserLookupResult:
    name: str
    email: str


@dataclass
class FakePlanLookupResult:
    max_number_accounts: int


class StubUserLookup:
    def __init__(self, result):
        self.result = result

    def execute(self, email: str):
        return self.result


class StubUserPlanLookup:
    def __init__(self, result):
        self.result = result

    def execute(self, email: str):
        return self.result


class StubBankAccountRepository:
    def __init__(self, count: int = 0):
        self.count = count
        self.created = []
        self.count_calls = []

    def count_by_user(self, user_email: str) -> int:
        self.count_calls.append(user_email)
        return self.count

    def create(self, bank_account):
        self.created.append(bank_account)


def build_body(initial_balance: Decimal = Decimal("250.75")) -> BankAccountCreate:
    return BankAccountCreate(
        name="Main account",
        bank_name="NuBank",
        account_number="123456",
        initial_balance=initial_balance,
    )


# --- happy path ---
def test_register_bank_account_creates_first_account_for_free_plan_user():
    repository = StubBankAccountRepository(count=0)
    user_lookup = StubUserLookup(
        FakeUserLookupResult(name="Aline", email="aline@example.com")
    )
    plan_lookup = StubUserPlanLookup(FakePlanLookupResult(max_number_accounts=1))

    register_bank_account(
        body=build_body(),
        email="aline@example.com",
        bank_account_repository=repository,
        query_user_by_email=user_lookup,
        query_user_plan=plan_lookup,
    )

    assert repository.count_calls == ["aline@example.com"]
    assert len(repository.created) == 1
    created_account = repository.created[0]
    assert created_account.name == "Main account"
    assert created_account.bank_name == "NuBank"
    assert created_account.account_number == "123456"
    assert created_account.balance == Decimal("250.75")
    assert created_account.user.name == "Aline"
    assert created_account.user.email == "aline@example.com"
    assert created_account.status == "active"


# --- error cases ---
def test_register_bank_account_raises_when_user_does_not_exist():
    repository = StubBankAccountRepository()

    with pytest.raises(
        UserNotFoundError, match="No user found with email: missing@example.com"
    ):
        register_bank_account(
            body=build_body(),
            email="missing@example.com",
            bank_account_repository=repository,
            query_user_by_email=StubUserLookup(None),
            query_user_plan=StubUserPlanLookup(FakePlanLookupResult(max_number_accounts=1)),
        )

    assert repository.count_calls == []
    assert repository.created == []


def test_register_bank_account_raises_when_user_has_no_active_plan():
    repository = StubBankAccountRepository()
    user_lookup = StubUserLookup(
        FakeUserLookupResult(name="Aline", email="aline@example.com")
    )

    with pytest.raises(
        NoActivePlanError, match="User does not have an active subscription plan."
    ):
        register_bank_account(
            body=build_body(),
            email="aline@example.com",
            bank_account_repository=repository,
            query_user_by_email=user_lookup,
            query_user_plan=StubUserPlanLookup(None),
        )

    assert repository.count_calls == []
    assert repository.created == []


def test_register_bank_account_raises_when_free_plan_limit_is_reached():
    repository = StubBankAccountRepository(count=1)
    user_lookup = StubUserLookup(
        FakeUserLookupResult(name="Aline", email="aline@example.com")
    )
    plan_lookup = StubUserPlanLookup(FakePlanLookupResult(max_number_accounts=1))

    with pytest.raises(
        AccountLimitReachedError,
        match=(
            "User has reached the maximum number of bank accounts allowed by their plan."
        ),
    ):
        register_bank_account(
            body=build_body(),
            email="aline@example.com",
            bank_account_repository=repository,
            query_user_by_email=user_lookup,
            query_user_plan=plan_lookup,
        )

    assert repository.count_calls == ["aline@example.com"]
    assert repository.created == []
