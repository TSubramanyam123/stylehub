from fastapi import APIRouter, HTTPException, status

from sqlalchemy import select

from app.dependencies import CurrentUser, DBSession
from app.models import User
from app.schemas import (
    Token,
    UserCreate,
    UserOut
)
from app.security import (
    create_access_token,
    hash_password,
    verify_password
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================
# REGISTER
# =========================

@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
def register(
    payload: UserCreate,
    db: DBSession
):

    email = payload.email.lower()

    existing_user = db.scalar(
        select(User).where(
            User.email == email
        )
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="Email is already registered"
        )

    user = User(
        email=email,
        hashed_password=hash_password(
            payload.password
        )
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


# =========================
# LOGIN
# =========================

@router.post(
    "/login",
    response_model=Token
)
def login(
    payload: UserCreate,
    db: DBSession
):

    # Find user using email
    user = db.scalar(
        select(User).where(
            User.email == payload.email.lower()
        )
    )

    # Check email and password
    if (
        not user
        or not verify_password(
            payload.password,
            user.hashed_password
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT token
    token = create_access_token(
        user.id
    )

    # Return Bearer access token
    return Token(
        access_token=token,
        token_type="bearer"
    )


# =========================
# CURRENT USER
# =========================

@router.get(
    "/me",
    response_model=UserOut
)
def me(
    current_user: CurrentUser
):

    return current_user