# app/routes/v1/users.py
from fastapi import APIRouter

router = APIRouter()


@router.get("/", response_model=list)
async def read_users():
    # Logic to retrieve users from a database or another data source
    return [{"user_id": 1, "username": "user1"}, {"user_id": 2, "username": "user2"}]


@router.get("/{user_id}", response_model=dict)
async def read_user(user_id: int):
    # Logic to retrieve a specific user by user_id
    return {"user_id": user_id, "username": f"user{user_id}"}


@router.post("/", response_model=dict)
async def create_user(user: dict):
    # Logic to create a new user
    # Save user to the database or perform necessary operations
    return user
