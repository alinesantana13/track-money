from app.authentication._user import User
from app.authentication._user_repository import UserRepository
from app.authentication.schema import UserCreate


class EmailAlreadyRegisteredError(Exception):
    pass


def register_user(body: UserCreate, user_repository: UserRepository) -> User:
    if user_repository.get_by_email(body.email):
        raise EmailAlreadyRegisteredError("Email already registered")
    user = User(name=body.name, email=body.email, password=body.password)
    user_repository.create(user)
    return user
