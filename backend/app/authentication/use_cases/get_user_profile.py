from app.authentication._user import User
from app.authentication._user_repository import UserRepository


class UserNotFoundError(Exception):
    pass


def get_user_profile(email: str, user_repository: UserRepository) -> User:
    user = user_repository.get_by_email(email)
    if not user:
        raise UserNotFoundError(f"No user found with email: {email}")
    return user
