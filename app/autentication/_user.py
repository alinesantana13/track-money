from sqlalchemy import Column, Integer, String

from app.autentication._password import get_password_hash, verify_password
from app.core.domain_error import DomainError
from app.infra.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "authentication"}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(512), nullable=False)

    def __init__(self, name: str, email: str, password: str):
        DomainError.validate(
            name and len(name) <= 128, "Name must be at most 128 characters long."
        )
        self.name = name

        DomainError.validate(
            email and "@" in email and len(email) <= 128,
            "Email must be a non-empty string with a maximum length of 128 characters."
        )
        self.email = email

        DomainError.validate(
            password and len(password) >= 8,
            "Password must be a non-empty string with a minimum length of 8 characters.",
        )
        self.hashed_password = get_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """
        Verify if the provided password matches the stored hashed password.
        """
        return verify_password(password, self.hashed_password)
