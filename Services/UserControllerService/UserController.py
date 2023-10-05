from bson import ObjectId

from Database.mongoDBConnection import database


class UserController:
    @staticmethod
    async def check_existing_email(email: str) -> bool:
        existing_user = await database.db.users.find_one({"email": email})
        return existing_user is not None

    @staticmethod
    async def check_existing_username(username: str) -> bool:
        existing_user = await database.db.users.find_one({"username": username})
        return existing_user is not None

    @staticmethod
    async def check_existing_mobile_number(mobile_number: str) -> bool:
        existing_user = await database.db.users.find_one({"mobile_number": mobile_number})
        return existing_user is not None

    @staticmethod
    async def find_user_by_id(user_id: str) -> dict:
        db_user = await database.db.users.find_one({'_id': ObjectId(user_id)})
        return db_user

    @staticmethod
    async def find_user(search_parameters: str, search_data: str):
        user = await database.db.users.find_one({search_parameters: search_data})
        return user

    @staticmethod
    def identify_user_data(data: str) -> str:
        if "@" in data and "." in data:
            return "email"
        elif data.isdigit() and len(data) == 10:
            return "mobile_number"
        else:
            return "username"
