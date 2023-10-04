from typing import List

from fastapi import APIRouter, HTTPException, Query

from Database.Schemas.UserSchema import ResponseUser, RegisterUser, RegisterResponseUser
from Services.UserControllerService.UserController import UserController

router = APIRouter()


@router.get("", response_model=List[ResponseUser])
async def read_users(user_id: str = Query(None)):
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
