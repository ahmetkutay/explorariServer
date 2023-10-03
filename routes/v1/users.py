from fastapi import APIRouter
from Database.Schemas.UserSchema import User
from Database.mongoDBConnection import database

router = APIRouter()


def transform_user_data(users_data):
    return [User(id=str(user["_id"]), user=user["user"]) for user in users_data]


@router.get("/", response_model=list[User])
async def read_users():
    users_data = await database.db.users.find({}).to_list(length=None)
    transformed_data = transform_user_data(users_data)
    return transformed_data
