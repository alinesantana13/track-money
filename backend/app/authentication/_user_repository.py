from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.authentication._user import User
from app.infra.database import get_db


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        """
        Create a new user in the database.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by email from the database.
        """
        return self.db.query(User).filter(User.email == email).first()


def get_user_repository(
    db: Annotated[Session, Depends(get_db)],
) -> UserRepository:
    return UserRepository(db)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
