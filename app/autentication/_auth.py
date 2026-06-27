import os

import pendulum
from jose import jwt

from app.autentication._user import User


def generate_jwt_token(user: User) -> str:
    """Generate a JWT token for the given user ID."""
    access_token_expires = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_secret_key = os.getenv("JWT_SECRET_KEY")
    algorithm = os.getenv("ALGORITHM", "HS256")

    if access_token_expires is None:
        raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES environment variable is not set.")
    if not jwt_secret_key:
        raise ValueError("JWT_SECRET_KEY environment variable is not set.")
    if not algorithm:
        raise ValueError("ALGORITHM environment variable is not set.")
    
    expire_minutes = int(access_token_expires)
    expire = pendulum.now("UTC") + pendulum.duration(minutes=expire_minutes)
    payload = {"sub": user.email, "name": user.name, "exp": expire}
    

    token = jwt.encode(payload, jwt_secret_key, algorithm=algorithm)
    return token
