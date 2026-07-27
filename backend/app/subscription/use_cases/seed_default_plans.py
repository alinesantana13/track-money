from app.subscription.plan._plan import Plan
from app.subscription.plan._plan_repository import PlanRepository

DEFAULT_PLANS = (
    {"name": "Free", "max_number_accounts": 1, "price": 0},
    {"name": "Premium", "max_number_accounts": 5, "price": 1990},
    {"name": "Enterprise", "max_number_accounts": 10, "price": 4990},
)


def seed_default_plans(plan_repository: PlanRepository) -> None:
    for plan_data in DEFAULT_PLANS:
        plan_repository.create_if_missing(
            Plan(
                name=plan_data["name"],
                max_number_accounts=plan_data["max_number_accounts"],
                price=plan_data["price"],
            )
        )
