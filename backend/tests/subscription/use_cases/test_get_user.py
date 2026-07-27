from dataclasses import dataclass

import pytest

from app.subscription.plan._plan import Plan
from app.subscription.use_cases.get_user import get_user
from app.subscription.user._user import User
from app.subscription.user._user_plan import UserPlan


@dataclass
class FakeUserLookupResult:
    name: str
    email: str


class StubUserLookup:
    def __init__(self, result):
        self.result = result
        self.requested_emails = []

    def execute(self, email: str):
        self.requested_emails.append(email)
        return self.result


class StubUserRepository:
    def __init__(self, existing_user: User | None, persisted_id: int = 1):
        self.existing_user = existing_user
        self.persisted_id = persisted_id
        self.requested_emails = []
        self.created = []

    def get_user_by_email(self, email: str) -> User | None:
        self.requested_emails.append(email)
        return self.existing_user

    def create(self, user: User):
        user.id = self.persisted_id
        self.created.append(user)
        self.existing_user = user


def build_plan(
    *,
    plan_id: int,
    name: str,
    max_number_accounts: int,
    price: int,
) -> Plan:
    plan = Plan(
        name=name,
        max_number_accounts=max_number_accounts,
        price=price,
    )
    plan.id = plan_id
    return plan


def attach_plan(user: User, plan: Plan, active: bool) -> None:
    user_plan = UserPlan(plan_id=plan.id, active=active)
    user_plan.plan = plan
    user.user_plans.append(user_plan)


# --- happy path ---
def test_get_user_returns_existing_user_with_prices_converted_from_cents_to_reais():
    user = User(name="Aline", email="aline@example.com")
    user.id = 7
    attach_plan(
        user,
        build_plan(plan_id=1, name="Free", max_number_accounts=1, price=0),
        active=False,
    )
    attach_plan(
        user,
        build_plan(plan_id=2, name="Premium", max_number_accounts=5, price=1999),
        active=True,
    )
    repository = StubUserRepository(existing_user=user)
    user_lookup = StubUserLookup(None)

    result = get_user("aline@example.com", repository, user_lookup)

    assert repository.requested_emails == ["aline@example.com"]
    assert repository.created == []
    assert user_lookup.requested_emails == []
    assert result.id == 7
    assert result.name == "Aline"
    assert result.email == "aline@example.com"
    assert len(result.plans) == 2
    assert result.plans[0].name == "Free"
    assert result.plans[0].price == 0.0
    assert result.plans[0].active is False
    assert result.plans[0].is_free is True
    assert result.plans[1].name == "Premium"
    assert result.plans[1].price == pytest.approx(19.99)
    assert result.plans[1].active is True
    assert result.plans[1].is_free is False


def test_get_user_creates_subscription_user_from_auth_context_when_missing():
    repository = StubUserRepository(existing_user=None, persisted_id=11)
    user_lookup = StubUserLookup(
        FakeUserLookupResult(name="Aline", email="aline@example.com")
    )

    result = get_user("aline@example.com", repository, user_lookup)

    assert repository.requested_emails == ["aline@example.com"]
    assert user_lookup.requested_emails == ["aline@example.com"]
    assert len(repository.created) == 1
    created_user = repository.created[0]
    assert created_user.id == 11
    assert created_user.name == "Aline"
    assert created_user.email == "aline@example.com"
    assert result.id == 11
    assert result.name == "Aline"
    assert result.email == "aline@example.com"
    assert result.plans == []


def test_get_user_uses_email_as_name_when_user_is_missing_in_all_contexts():
    repository = StubUserRepository(existing_user=None, persisted_id=13)
    user_lookup = StubUserLookup(None)

    result = get_user("missing@example.com", repository, user_lookup)

    assert repository.requested_emails == ["missing@example.com"]
    assert user_lookup.requested_emails == ["missing@example.com"]
    assert len(repository.created) == 1
    created_user = repository.created[0]
    assert created_user.id == 13
    assert created_user.name == "missing@example.com"
    assert created_user.email == "missing@example.com"
    assert result.id == 13
    assert result.name == "missing@example.com"
    assert result.email == "missing@example.com"
    assert result.plans == []
