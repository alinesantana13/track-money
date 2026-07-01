from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.autentication.get_email_from_token import EmailFromTokenDep
from app.autentication.query_user_by_email import QueryUserByEmailDep
from app.movement.bank._bank_account_repository import BankAccountRepositoryDep
from app.movement.schema import BankAccountCreate
from app.movement.use_cases.register_bank_account import (
    AccountLimitReachedError,
    NoActivePlanError,
    UserNotFoundError,
    register_bank_account,
)
from app.subscription.query_user_plan import QueryUserPlanDep

router = APIRouter()


@router.post(
    "/bank-accounts",
    status_code=201,
    tags=["movement"],
    summary="Create a new bank account",
)
def create_bank_account(
    body: BankAccountCreate,
    email: EmailFromTokenDep,
    bank_account_repository: BankAccountRepositoryDep,
    query_user_by_email: QueryUserByEmailDep,
    query_user_plan: QueryUserPlanDep,
):
    try:
        register_bank_account(
            body, email, bank_account_repository, query_user_by_email, query_user_plan
        )
    except UserNotFoundError as e:
        return JSONResponse(status_code=404, content={"detail": str(e)})
    except NoActivePlanError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})
    except AccountLimitReachedError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})
    return JSONResponse(
        status_code=201,
        content={"message": "Bank account created successfully"},
    )