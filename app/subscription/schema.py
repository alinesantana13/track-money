from pydantic import BaseModel


class SelectPlan(BaseModel):
    plan_id: int


class PlanResponse(BaseModel):
    id: int
    name: str
    price: float
    active: bool
    is_free: bool


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    plans: list[PlanResponse] = []