from app.autentication import QueryUserByEmail
from app.subscription.schema import PlanResponse, UserResponse
from app.subscription.user._user import User
from app.subscription.user._user_repository import UserRepository


def get_user(
    email: str,
    user_repository: UserRepository,
    query_user_by_email: QueryUserByEmail,
) -> UserResponse:
    """
    Get a user by email. If the user does not exist in the subscription context,
    fetch their name from the authentication context.
    """
    user = user_repository.get_user_by_email(email)
    if not user:
        user_auth = query_user_by_email.execute(email)
        user = User(name=user_auth.name if user_auth else email, email=email)

    plans = [
        PlanResponse(
            id=up.plan.id,
            name=up.plan.name,
            price=up.plan.price,
            active=up.active,
            is_free=up.plan.is_free
        ) for up in user.user_plans
    ]

    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        plans=plans
    )

