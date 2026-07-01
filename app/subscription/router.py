from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.authentication import EmailFromTokenDep, QueryUserByEmailDep
from app.subscription.plan._plan_repository import PlanRepositoryDep
from app.subscription.schema import SelectPlan
from app.subscription.use_cases.get_user import get_user
from app.subscription.use_cases.select_plan import PlanNotFoundError, select_plan
from app.subscription.user._user_repository import UserRepositoryDep

router = APIRouter()


@router.post(
    "/select-plan",
    response_model=None,
    status_code=200,
    tags=["subscription"],
    summary="Select a subscription plan for the authenticated user",
)
def select_user_plan(
    body: SelectPlan,
    email: EmailFromTokenDep,
    user_repository: UserRepositoryDep,
    plan_repository: PlanRepositoryDep,
    query_user_by_email: QueryUserByEmailDep,
):
    try:
        select_plan(email, body, user_repository, plan_repository, query_user_by_email)
    except PlanNotFoundError as e:
        return JSONResponse(status_code=404, content={"detail": str(e)})


@router.get(
    "/user",
    response_model=None,
    status_code=200,
    tags=["subscription"],
    summary="Get the authenticated user's subscription plans",
)
def get_user_plans(
    email: EmailFromTokenDep,
    user_repository: UserRepositoryDep,
    query_user_by_email: QueryUserByEmailDep,
):
    user_response = get_user(email, user_repository, query_user_by_email)
    return JSONResponse(status_code=200, content=user_response.model_dump())
