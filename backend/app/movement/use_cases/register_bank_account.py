from decimal import Decimal

from app.movement.bank._bank_account import BankAccount, User
from app.movement.bank._bank_account_repository import BankAccountRepository
from app.movement.schema import BankAccountCreate
from app.movement.use_cases._ports import UserLookupPort, UserPlanLookupPort


class UserNotFoundError(Exception):
    pass


class NoActivePlanError(Exception):
    pass


class AccountLimitReachedError(Exception):
    pass


def register_bank_account(
        body: BankAccountCreate,
        email: str,
        bank_account_repository: BankAccountRepository,
        query_user_by_email: UserLookupPort,
        query_user_plan: UserPlanLookupPort,
    ) -> None:
    user_auth = query_user_by_email.execute(email)
    if not user_auth:
        raise UserNotFoundError(f"No user found with email: {email}")

    user_plan = query_user_plan.execute(email)
    if not user_plan:
        raise NoActivePlanError("User does not have an active subscription plan.")

    account_count = bank_account_repository.count_by_user(email)
    if account_count >= user_plan.max_number_accounts:
        raise AccountLimitReachedError(
            "User has reached the maximum number of bank accounts allowed by their plan."
        )

    user = User(name=user_auth.name, email=user_auth.email)
    bank_account = BankAccount(
        name=body.name,
        bank_name=body.bank_name,
        account_number=body.account_number,
        user=user,
        balance=Decimal(str(body.initial_balance)),
    )
    bank_account_repository.create(bank_account)