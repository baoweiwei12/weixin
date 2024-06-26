from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.core import dependencies, security

router = APIRouter(prefix="", tags=["auth"])


@router.post("/login/token", response_model=security.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(dependencies.get_db),
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.username})
    return security.Token(access_token=access_token, token_type="bearer")


@router.post("/refresh/token", response_model=security.Token)
def refresh_access_token(
    current_user: models.User = Depends(dependencies.get_current_active_user),
    db: Session = Depends(dependencies.get_db),
):
    access_token = security.create_access_token(data={"sub": current_user.username})
    return security.Token(access_token=access_token, token_type="bearer")


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


@router.post("/register", response_model=schemas.User)
def register_user(
    user: UserRegister,
    db: Session = Depends(dependencies.get_db),
):
    if crud.get_user_by_username(db, username=user.username) or crud.get_user_by_email(
        db, email=user.email
    ):
        raise HTTPException(
            status_code=400, detail="Username or email already registered"
        )
    db_user = crud.create_user(
        db,
        user=schemas.UserCreate(
            username=user.username,
            email=user.email,
            password=user.password,
            role="user",
        ),
    )
    return db_user
