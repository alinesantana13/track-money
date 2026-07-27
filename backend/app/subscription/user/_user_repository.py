from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.subscription.user._user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User):
        """
        Create a new user in the database.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
  

    def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieve a user from the database by their email address.
        """
        return self.db.query(User).filter(User.email == email).first()


def get_user_repository(db: Annotated[Session, Depends(get_db)]) -> UserRepository:
    """
    Dependency injection for UserRepository.
    """
    return UserRepository(db)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]