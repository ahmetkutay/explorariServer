from typing import Union, Any

from pydantic import BaseModel


class ResponseModel(BaseModel):
    status: bool
    message: Union[str, None] = None
    data: Any = None
