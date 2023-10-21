import random
from array import array
from datetime import datetime, timedelta

from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field

from Configs.settings import JWT_EXPIRE_MINUTES
from Database.mongoDBConnection import database
from Helpers.Auth import create_access_token
from Services.UserControllerService.UserController import UserController

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ResponseUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    mobile_number: str
    verified: bool
    token: str
    refresh_token: str
    created_at: datetime
    updated_at: datetime


class RegisterResponseUser(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    mobile_number: str
    verified: bool
    verification_code: int
    token: str
    refresh_token: str


class RegisterUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    mobile_number: str
    verified: bool = Field(default=False, alias="verified")
    verification_code: int = 100000 + random.randint(0, 900000)
    token: str = ""
    refresh_token: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="created_at")
    updated_at: datetime = Field(default_factory=datetime.utcnow, alias="updated_at")

    def hash_password(self):
        self.password = pwd_context.hash(self.password)

    async def register(self):
        # Check if the user already exists
        if await UserController.check_existing_email(self.email):
            raise Exception("Email already exists")
        if await UserController.check_existing_username(self.username):
            raise Exception("Username already exists")
        if await UserController.check_existing_mobile_number(self.mobile_number):
            raise Exception("Mobile number already exists")

        # Hash the password
        self.hash_password()

        # Store the user data in the database (assuming 'users' is your collection name)
        result = await database.db.users.insert_one(self.model_dump())
        user_id = result.inserted_id
        # Return the registered user response
        registered_user = RegisterResponseUser(
            id=str(user_id),
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            mobile_number=self.mobile_number,
            verified=self.verified,
            verification_code=self.verification_code,
            access_token=self.token,
            refresh_token=self.refresh_token
        )
        return registered_user


class LoginRequestModel(BaseModel):
    username: str
    password: str

    def login(self: ResponseUser, user: array, password: str):
        if self and pwd_context.verify(password, user['password']):
            return True
        else:
            return None
