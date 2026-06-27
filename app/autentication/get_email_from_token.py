import os
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


def get_email_from_token(
    token: Annotated[str, Depends(_oauth2_scheme)],
) -> str:
    """Decode the JWT token and return the email."""
    try:
        jwt_secret_key = os.getenv("JWT_SECRET_KEY")
        algorithm = os.getenv("ALGORITHM", "HS256")

        if not jwt_secret_key:
            raise ValueError("JWT_SECRET_KEY environment variable is not set.")
        if not algorithm:
            raise ValueError("ALGORITHM environment variable is not set.")

        payload = jwt.decode(token, jwt_secret_key, algorithms=[algorithm])

        email = payload.get("sub")

        if not email:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
            )
        return email
    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        ) from None
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}",
        ) from e


EmailFromTokenDep = Annotated[str, Depends(get_email_from_token)]
