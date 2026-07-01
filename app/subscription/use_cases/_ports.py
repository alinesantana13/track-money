from typing import Protocol


class UserLookupResult(Protocol):
    name: str
    email: str


class UserLookupPort(Protocol):
    """
    Port for looking up a user by email from outside the subscription context.
    Any adapter (e.g. QueryUserByEmail from the authentication context) that
    implements an `execute` method with this signature satisfies this protocol.
    """

    def execute(self, email: str) -> UserLookupResult | None: ...
