from app.autentication import QueryUserByEmail
from app.subscription.plan._plan_repository import PlanRepository
from app.subscription.schema import SelectPlan
from app.subscription.user._user import User
from app.subscription.user._user_repository import UserRepository


class PlanNotFoundError(Exception):
    pass


def select_plan(
    email: str,
    body: SelectPlan,
    user_repository: UserRepository,
    plan_repository: PlanRepository,
    query_user_by_email: QueryUserByEmail,
) -> None:
    """
    Assigns a subscription plan to the authenticated user.
    Creates the user in the subscription context if they don't exist yet.
    """
    user = user_repository.get_user_by_email(email)
    if not user:
        user_auth = query_user_by_email.execute(email)
        user = User(name=user_auth.name if user_auth else email, email=email)

    plan = plan_repository.get_plan_by_id(body.plan_id)
    if not plan:
        raise PlanNotFoundError(f"Plan {body.plan_id} not found.")

    user.add_plan(plan)
    user_repository.create(user)
