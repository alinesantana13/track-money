from app.subscription.plan._plan import Plan
from app.subscription.use_cases.list_plans import list_plans


class StubPlanRepository:
    def __init__(self, plans: list[Plan]):
        self.plans = plans
        self.list_calls = 0

    def list_plans(self) -> list[Plan]:
        self.list_calls += 1
        return self.plans


def test_list_plans_returns_available_plans():
    plans = [
        Plan(name="Free", max_number_accounts=1, price=0),
        Plan(name="Premium", max_number_accounts=5, price=1990),
    ]
    repository = StubPlanRepository(plans)

    result = list_plans(repository)

    assert result == plans
    assert repository.list_calls == 1
