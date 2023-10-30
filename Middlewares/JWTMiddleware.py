from fastapi import HTTPException, status
import jwt
from Configs.settings import ENCRYPT_PASSWORD
from Helpers.AuthHelper import TokenData, decode_token
from starlette.middleware.base import BaseHTTPMiddleware
from Helpers.Encryptions import EncryptionHandler
from Services.UserControllerService import UserController


class JWTMiddleware(BaseHTTPMiddleware):
    EXCLUDED_PATHS = ["/api/auth/register", "/api/auth/login"]

    async def dispatch(self, request, call_next):
        if request.url.path in self.EXCLUDED_PATHS:
            response = await call_next(request)
            return response

        token = request.headers.get("Authorization", None)
        if token is None or not token.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = token.split(" ")[1]
        try:
            payload = decode_token(token)
            payload_sub_id = payload.get("sub")
            sub_id = EncryptionHandler(ENCRYPT_PASSWORD).decrypt(payload_sub_id)
            user = await UserController.UserController.find_user_by_id(sub_id)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload",
                )
            token_data = TokenData(username=user['username'])
            request.state.token_data = token_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        response = await call_next(request)
        return response
