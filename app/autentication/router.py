from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.autentication._auth import get_email_from_token
from app.autentication.schema import TokenResponse, UserCreate, UserProfileResponse
from app.autentication.use_cases.authenticate_user import (
    InvalidCredentialsError,
    authenticate_user,
)
from app.autentication.use_cases.get_user_profile import (
    UserNotFoundError,
    get_user_profile,
)
from app.autentication.use_cases.register_user import (
    EmailAlreadyRegisteredError,
    register_user,
)
from app.autentication.user_repository import UserRepository, get_user_repository

router = APIRouter()


@router.post("", response_model=None, tags=["users"], summary="Create a new user")
def create_user(
    body: UserCreate, user_repository: UserRepository = Depends(get_user_repository)
):
    try:
        user = register_user(body, user_repository)
    except EmailAlreadyRegisteredError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    return JSONResponse(
        status_code=201,
        content={"message": "User created successfully", "user_id": user.id},
        headers={"Location": f"/users/{user.id}"},
    )


@router.post(
    "/token",
    response_model=TokenResponse,
    tags=["users"],
    summary="Create a JWT token for the user",
)
def create_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repository: UserRepository = Depends(get_user_repository),
) -> TokenResponse:
    try:
        token = authenticate_user(form_data.username, form_data.password, user_repository)
    except InvalidCredentialsError:
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})
    return TokenResponse(access_token=token)


@router.get(
    "/profile",
    response_model=UserProfileResponse,
    tags=["users"],
    summary="Get the profile of the authenticated user",
)
def user_profile(
    email: str = Depends(get_email_from_token),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserProfileResponse:
    try:
        user = get_user_profile(email, user_repository)
    except UserNotFoundError:
        return JSONResponse(status_code=404, content={"detail": "User not found"})
    return UserProfileResponse(email=user.email, name=user.name)