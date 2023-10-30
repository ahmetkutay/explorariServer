from datetime import timedelta
from typing import List

from fastapi import APIRouter, HTTPException, Query, status

from Configs.settings import JWT_EXPIRE_MINUTES
from Database.Schemas.UserSchema import ResponseUser, RegisterUser, RegisterResponseUser, LoginRequestModel
from Helpers.AuthHelper import create_access_token, encrypt_user_data
from Services.UserControllerService.UserController import UserController

router = APIRouter()


@router.get("", response_model=List[ResponseUser])
async def check_logged_in_or_log_in(user_id: str = Query(None)):
    try:
        user_data = await UserController.find_user_by_id(user_id)
        if user_data:
            return [user_data]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Find User failed: {str(e)}")


@router.post("/register", response_model=RegisterResponseUser)
async def register_user(user_data: RegisterUser):
    try:
        registered_user = await user_data.register()
        return registered_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")


@router.post("/login")
async def login(login_data: LoginRequestModel):
    username = login_data.username
    password = login_data.password
    search_parameter = UserController.identify_user_data(username)
    user = await UserController.find_user(search_parameter, username)
    if user and login_data.login(user, password):
        access_token_expires = timedelta(minutes=float(JWT_EXPIRE_MINUTES))
        encrypted_user = encrypt_user_data(user)
        access_token = create_access_token(
            data=encrypted_user, expires_delta=access_token_expires
        )
        await UserController.set_access_token(user['_id'], access_token)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
