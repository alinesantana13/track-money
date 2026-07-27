import pytest

from app.authentication.schema import UserCreate
from app.authentication.use_cases.register_user import (
    EmailAlreadyRegisteredError,
    register_user,
)
from app.core.domain_error import DomainError


class StubUserRepository:
    def __init__(self, existing_user=None):
        self.existing_user = existing_user
        self.created_users = []

    def get_by_email(self, email: str):
        return self.existing_user

    def create(self, user):
        self.created_users.append(user)
        return user


# --- happy path ---
def test_register_user_creates_user_when_email_is_available():
    repository = StubUserRepository()
    body = UserCreate(
        name="Aline",
        email="aline@example.com",
        password="strongpass123",
    )

    user = register_user(body, repository)

    assert user.name == body.name
    assert user.email == body.email
    assert user.hashed_password != body.password
    assert user.verify_password(body.password) is True
    assert repository.created_users == [user]


# --- error cases ---
def test_register_user_raises_when_email_is_already_registered():
    repository = StubUserRepository(existing_user=object())
    body = UserCreate(
        name="Aline",
        email="aline@example.com",
        password="strongpass123",
    )

    with pytest.raises(EmailAlreadyRegisteredError, match="Email already registered"):
        register_user(body, repository)

    assert repository.created_users == []


def test_register_user_raises_domain_error_when_name_is_too_long():
    repository = StubUserRepository()
    body = UserCreate(
        name="a" * 129,
        email="aline@example.com",
        password="strongpass123",
    )

    with pytest.raises(DomainError) as exc_info:
        register_user(body, repository)

    assert str(exc_info.value) == "Name must be at most 128 characters long."
    assert repository.created_users == []


def test_register_user_raises_domain_error_when_email_is_invalid():
    repository = StubUserRepository()
    body = UserCreate(
        name="Aline",
        email="invalid-email",
        password="strongpass123",
    )

    with pytest.raises(DomainError) as exc_info:
        register_user(body, repository)

    assert (
        str(exc_info.value)
        == "Email must be a non-empty string with a maximum length of 128 characters."
    )
    assert repository.created_users == []


def test_register_user_raises_domain_error_when_password_is_too_short():
    repository = StubUserRepository()
    body = UserCreate(
        name="Aline",
        email="aline@example.com",
        password="short",
    )

    with pytest.raises(DomainError) as exc_info:
        register_user(body, repository)

    assert (
        str(exc_info.value)
        == "Password must be a non-empty string with a minimum length of 8 characters."
    )
    assert repository.created_users == []


def test_register_user_raises_domain_error_when_password_exceeds_bcrypt_limit():
    repository = StubUserRepository()
    body = UserCreate(
        name="Aline",
        email="aline@example.com",
        password="á" * 37,
    )

    with pytest.raises(DomainError) as exc_info:
        register_user(body, repository)

    assert (
        str(exc_info.value)
        == "Password must be at most 72 bytes in UTF-8 for bcrypt compatibility."
    )
    assert repository.created_users == []
