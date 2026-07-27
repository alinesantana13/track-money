import pytest

from app.core.domain_error import DomainError
from app.subscription.plan._plan import Plan
from app.subscription.user._user import User


# --- error cases ---
def test_user_add_free_plan_rejects_paid_plan():
    user = User(name="Aline", email="aline@example.com")
    paid_plan = Plan(name="Premium", max_number_accounts=5, price=1990)

    with pytest.raises(DomainError) as exc_info:
        user.add_free_plan(paid_plan)

    assert str(exc_info.value) == "Only free plans can be activated without checkout."
