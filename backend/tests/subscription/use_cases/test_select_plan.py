from dataclasses import dataclass

import pytest

from app.subscription.plan._plan import Plan
from app.subscription.schema import SelectPlan
from app.subscription.use_cases.select_plan import (
    PaidPlanRequiresCheckoutError,
    select_plan,
)


@dataclass
class FakeUserLookupResult:
    name: str
    email: str


class StubPlanRepository:
    def __init__(self, plan: Plan):
        self.plan = plan
        self.requested_plan_ids = []

    def get_plan_by_id(self, plan_id: int) -> Plan:
        self.requested_plan_ids.append(plan_id)
        return self.plan


class StubUserRepository:
    def __init__(self):
        self.requested_emails = []
        self.created = []

    def get_user_by_email(self, email: str):
        self.requested_emails.append(email)
        return None

    def create(self, user):
        self.created.append(user)


class StubUserLookup:
    def __init__(self, result):
        self.result = result
        self.requested_emails = []

    def execute(self, email: str):
        self.requested_emails.append(email)
        return self.result


def build_plan(*, plan_id: int, price: int) -> Plan:
    plan = Plan(
        name="Free" if price == 0 else "Premium",
        max_number_accounts=1 if price == 0 else 5,
        price=price,
    )
    plan.id = plan_id
    return plan


# --- happy path ---
def test_select_plan_creates_user_and_assigns_selected_free_plan():
    plan = build_plan(plan_id=1, price=0)
    plan_repository = StubPlanRepository(plan)
    user_repository = StubUserRepository()
    user_lookup = StubUserLookup(
        FakeUserLookupResult(name="Aline", email="aline@example.com")
    )

    select_plan(
        "aline@example.com",
        SelectPlan(plan_id=1),
        user_repository,
        plan_repository,
        user_lookup,
    )

    assert plan_repository.requested_plan_ids == [1]
    assert user_repository.requested_emails == ["aline@example.com"]
    assert user_lookup.requested_emails == ["aline@example.com"]
    assert len(user_repository.created) == 1
    created_user = user_repository.created[0]
    assert created_user.name == "Aline"
    assert created_user.email == "aline@example.com"
    assert len(created_user.user_plans) == 1
    assert created_user.user_plans[0].plan_id == 1
    assert created_user.user_plans[0].active is True


# --- error cases ---
def test_select_plan_rejects_paid_plan_without_looking_up_or_persisting_user():
    plan_repository = StubPlanRepository(build_plan(plan_id=2, price=1990))
    user_repository = StubUserRepository()
    user_lookup = StubUserLookup(
        FakeUserLookupResult(name="Aline", email="aline@example.com")
    )

    with pytest.raises(PaidPlanRequiresCheckoutError):
        select_plan(
            "aline@example.com",
            SelectPlan(plan_id=2),
            user_repository,
            plan_repository,
            user_lookup,
        )

    assert plan_repository.requested_plan_ids == [2]
    assert user_repository.requested_emails == []
    assert user_repository.created == []
    assert user_lookup.requested_emails == []
