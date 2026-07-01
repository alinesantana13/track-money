from decimal import Decimal

import pytest

from app.core.domain_error import DomainError
from app.movement.bank._bank_account import AccountStatus, BankAccount, User


def build_user() -> User:
    return User(name="Aline", email="aline@example.com")


# --- happy path ---
def test_user_value_object_accepts_valid_name_and_email():
    user = build_user()

    assert user.name == "Aline"
    assert user.email == "aline@example.com"
    assert user.__composite_values__() == ("Aline", "aline@example.com")


def test_bank_account_sets_active_status_and_preserves_balance():
    account = BankAccount(
        name="Emergency fund",
        bank_name="NuBank",
        account_number="ACC123",
        user=build_user(),
        balance=Decimal("500.25"),
    )

    assert account.name == "Emergency fund"
    assert account.bank_name == "NuBank"
    assert account.account_number == "ACC123"
    assert account.user.email == "aline@example.com"
    assert account.balance == Decimal("500.25")
    assert account.status == AccountStatus.ACTIVE.value


def test_bank_account_defaults_balance_to_zero():
    account = BankAccount(
        name="Savings",
        bank_name="NuBank",
        account_number="ACC123",
        user=build_user(),
    )

    assert account.balance == Decimal("0")
    assert account.status == AccountStatus.ACTIVE.value


# --- error cases ---
@pytest.mark.parametrize(
    ("name", "email", "message"),
    [
        ("a" * 129, "aline@example.com", "Name must be at most 128 characters long."),
        ("Aline", "invalid-email", "Email must be a non-empty string with a maximum length of 128 characters."),
    ],
)
def test_user_value_object_rejects_invalid_data(name: str, email: str, message: str):
    with pytest.raises(DomainError) as exc_info:
        User(name=name, email=email)

    assert str(exc_info.value) == message


@pytest.mark.parametrize(
    ("field_name", "value", "message"),
    [
        ("name", "a" * 25, "Name must be at most 24 characters long."),
        ("bank_name", "b" * 25, "Bank name must be at most 24 characters long."),
        ("account_number", "1" * 25, "Account number must be at most 24 characters long."),
    ],
)
def test_bank_account_rejects_text_fields_longer_than_24_chars(
    field_name: str, value: str, message: str
):
    kwargs = {
        "name": "Checking",
        "bank_name": "NuBank",
        "account_number": "ACC123",
        "user": build_user(),
        "balance": Decimal("10.00"),
    }
    kwargs[field_name] = value

    with pytest.raises(DomainError) as exc_info:
        BankAccount(**kwargs)

    assert str(exc_info.value) == message


def test_bank_account_rejects_negative_balance():
    with pytest.raises(DomainError) as exc_info:
        BankAccount(
            name="Checking",
            bank_name="NuBank",
            account_number="ACC123",
            user=build_user(),
            balance=Decimal("-0.01"),
        )

    assert str(exc_info.value) == "Balance must be a non-negative decimal number."
