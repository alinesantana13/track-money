from app.subscription.plan._plan import Plan
from app.subscription.plan._plan_repository import PlanRepository


def list_plans(plan_repository: PlanRepository) -> list[Plan]:
    return plan_repository.list_plans()
