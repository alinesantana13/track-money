from app.subscription.use_cases.seed_default_plans import (
    DEFAULT_PLANS,
    seed_default_plans,
)


class StubPlanRepository:
    def __init__(self, existing_names: set[str] | None = None):
        self.existing_names = set(existing_names or set())
        self.created = []

    def create_if_missing(self, plan):
        if plan.name in self.existing_names:
            return None
        self.created.append(plan)
        self.existing_names.add(plan.name)
        return None


def test_seed_default_plans_creates_missing_defaults():
    repository = StubPlanRepository(existing_names={"Free"})

    seed_default_plans(repository)

    created_names = [plan.name for plan in repository.created]
    assert created_names == ["Premium", "Enterprise"]


def test_seed_default_plans_creates_expected_default_catalog_values():
    repository = StubPlanRepository()

    seed_default_plans(repository)

    created_plans = [
        (plan.name, plan.max_number_accounts, plan.price, plan.is_free)
        for plan in repository.created
    ]
    assert created_plans == [
        ("Free", 1, 0, True),
        ("Premium", 5, 1990, False),
        ("Enterprise", 10, 4990, False),
    ]


def test_seed_default_plans_is_idempotent_when_defaults_exist():
    repository = StubPlanRepository(
        existing_names={plan["name"] for plan in DEFAULT_PLANS}
    )

    seed_default_plans(repository)

    assert repository.created == []
