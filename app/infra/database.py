import os

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


_engine: Engine | None = None
_session_local: sessionmaker | None = None

def get_engine() -> Engine:
    global _engine
    if _engine is None:
        if not os.getenv("DATABASE_URL"):
            raise ValueError("DATABASE_URL environment variable is not set.")

        _engine = create_engine(os.getenv("DATABASE_URL"))
    return _engine

def get_session_local() -> sessionmaker:
    global _session_local
    if _session_local is None:
        _session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine()
        )
    return _session_local

def get_db():
    session_local = get_session_local()
    db = session_local()
    try:
        yield db
    finally:
        db.close()

def init_database():
    engine = get_engine()
    with engine.connect() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS authentication"))
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS subscription"))
        connection.commit()

def create_tables():
    engine = get_engine()
    from app.autentication._user import (
        User,  # noqa: F401 - Import required to register the model with SQLAlchemy
    )
    from app.subscription.plan._plan import (
        Plan,  # noqa: F401 - Import required to register the model with SQLAlchemy
    )
    from app.subscription.user._user_plan import (
        UserPlan,  # noqa: F401 - Import required to register the model with SQLAlchemy
    )
    Base.metadata.create_all(bind=engine)