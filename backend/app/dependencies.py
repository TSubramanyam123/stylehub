from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.security import decode_access_token


# ==========================================
# DATABASE
# ==========================================

DBSession = Annotated[
    Session,
    Depends(get_db)
]


# ==========================================
# BEARER AUTHENTICATION
# ==========================================

bearer_scheme = HTTPBearer()


# ==========================================
# GET CURRENT USER
# ==========================================

def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(bearer_scheme)
    ],
    db: DBSession
) -> User:

    # Get JWT token from:
    #
    # Authorization: Bearer <token>
    #
    token = credentials.credentials

    # Decode JWT
    user_id = decode_access_token(token)

    if user_id is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    # Find user
    user = db.get(
        User,
        user_id
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


# ==========================================
# CURRENT USER TYPE
# ==========================================

CurrentUser = Annotated[
    User,
    Depends(get_current_user)
]