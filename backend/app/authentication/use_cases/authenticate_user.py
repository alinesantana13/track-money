from app.authentication._auth import generate_jwt_token
from app.authentication._user_repository import UserRepository


class InvalidCredentialsError(Exception):
    pass


def authenticate_user(email: str, password: str, user_repository: UserRepository) -> str:
    user = user_repository.get_by_email(email)
    if not user or not user.verify_password(password):
        raise InvalidCredentialsError("Invalid credentials")
    return generate_jwt_token(user)
