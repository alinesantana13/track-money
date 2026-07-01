import pytest

from app.core.domain_error import DomainError
from app.subscription.plan._plan import Plan


# --- happy path ---
def test_plan_sets_is_free_true_when_price_is_zero():
    plan = Plan(name="Free", max_number_accounts=1, price=0)

    assert plan.name == "Free"
    assert plan.max_number_accounts == 1
    assert plan.price == 0
    assert plan.is_free is True
    assert plan.created_at is not None


def test_plan_sets_is_free_false_when_price_is_positive():
    plan = Plan(name="Premium", max_number_accounts=5, price=1990)

    assert plan.is_free is False


# --- error cases ---
@pytest.mark.parametrize(
    ("name", "message"),
    [
        ("", "Plan name must be a non-empty string with a maximum length of 24 characters."),
        ("p" * 25, "Plan name must be a non-empty string with a maximum length of 24 characters."),
    ],
)
def test_plan_rejects_invalid_name(name: str, message: str):
    with pytest.raises(DomainError) as exc_info:
        Plan(name=name, max_number_accounts=1, price=0)

    assert str(exc_info.value) == message


def test_plan_rejects_negative_max_number_accounts():
    with pytest.raises(DomainError) as exc_info:
        Plan(name="Premium", max_number_accounts=-1, price=1990)

    assert str(exc_info.value) == "Max number of accounts must be a non-negative integer."
