from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.authentication import EmailFromTokenDep, QueryUserByEmailDep
from app.movement.bank._bank_account_repository import BankAccountRepositoryDep
from app.movement.schema import BankAccountCreate, BankAccountResponse
from app.movement.use_cases.list_bank_accounts import list_bank_accounts
from app.movement.use_cases.register_bank_account import (
    AccountLimitReachedError,
    NoActivePlanError,
    UserNotFoundError,
    register_bank_account,
)
from app.subscription.query_user_plan import QueryUserPlanDep

router = APIRouter()


@router.get(
    "/bank-accounts",
    response_model=list[BankAccountResponse],
    status_code=200,
    tags=["movement"],
    summary="List the authenticated user's bank accounts",
)
def get_bank_accounts(
    email: EmailFromTokenDep,
    bank_account_repository: BankAccountRepositoryDep,
) -> list[BankAccountResponse]:
    bank_accounts = list_bank_accounts(email, bank_account_repository)
    return [
        BankAccountResponse(
            id=bank_account.id,
            name=bank_account.name,
            bank_name=bank_account.bank_name,
            account_number=bank_account.account_number,
            balance=float(bank_account.balance),
            status=bank_account.status,
        )
        for bank_account in bank_accounts
    ]


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