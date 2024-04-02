from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from webchat.db.repository import Repo
from webchat.servises import verify_password, create_access_token
from webchat.dependencies import get_repository, get_session
from webchat.models import (
    RegisterRequest,
    LoginRequest,
    LoginUser,
    RegisterUser,
)


router = APIRouter()


@router.post("/login")
async def login(
    user: LoginRequest,
    session: AsyncSession = Depends(get_session),
    repository: Repo= Depends(get_repository)
):
    user: LoginUser = user.user

    user_db = await repository.get_user_by_username(session, user.username)
    if not user_db or not verify_password(user.password, user_db.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    data = {"username": user_db.username, "id": user_db.id}
    return {"user": data, "token": create_access_token(data)}


@router.post("/register")
async def register(
    user: RegisterRequest,
    session: AsyncSession = Depends(get_session),
    repository: Repo= Depends(get_repository)
):
    user: RegisterUser = user.user
    if user.password != user.confirmation_password:
        raise HTTPException(status_code=400, detail="Password is not equal")

    users_db = await repository.get_user_by_username(session, user.username)
    if users_db:
        print(users_db)
        raise HTTPException(status_code=400, detail="Username already registered")
    user = await repository.create_user(session, user.username, user.password)
    return {"username": user.username, "message": "User successfully registered"}
