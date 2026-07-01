from typing import Protocol


class UserLookupResult(Protocol):
    name: str
    email: str


class UserLookupPort(Protocol):
    """
    Port for looking up a user by email from outside the movement context.
    Any adapter that implements an `execute` method with this signature
    (e.g. QueryUserByEmail from the autentication context) satisfies this protocol.
    """

    def execute(self, email: str) -> UserLookupResult | None: ...


class UserPlanLookupResult(Protocol):
    max_number_accounts: int


class UserPlanLookupPort(Protocol):
    """
    Port for looking up a user's active plan limits from outside the movement context.
    Any adapter that implements an `execute` method with this signature
    (e.g. QueryUserPlan from the subscription context) satisfies this protocol.
    """

    def execute(self, email: str) -> UserPlanLookupResult | None: ...

