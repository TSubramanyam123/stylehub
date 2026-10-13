from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from jwt.exceptions import InvalidTokenError

from app.core.config import settings


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(
    password: str,
    hashed_password: str
) -> bool:

    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )

    except (ValueError, TypeError):
        return False


def create_access_token(user_id: int) -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )


def decode_access_token(token: str) -> int | None:

    try:

        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )

        sub = payload.get("sub")

        return int(sub) if sub is not None else None

    except (
        InvalidTokenError,
        ValueError,
        TypeError
    ):
        return None