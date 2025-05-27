from typing import Optional, Any, TypeVar, Generic

from pydantic import BaseModel, ConfigDict

DataT = TypeVar("DataT")

class BaseResponse(BaseModel, Generic[DataT]):
    model_config = ConfigDict(from_attributes=True)

    code: str
    message: str
    data: Optional[DataT] = None

class SuccessResponse(BaseResponse[Any]):
    pass

class ErrorResponse(BaseResponse[None]):
    pass

def res_success(data: Any = None, code: str = "0", message: str = "success") -> BaseResponse:
    return BaseResponse(code=code, message=message, data=data)

def res_ok(data: Any = None, code: str = "0", message: str = "ok") -> BaseResponse:
    return res_success(data=data, code=code, message=message)

def res_error(code: str = "0", message: str = "error") -> BaseResponse:
    return BaseResponse(code=code, message=message, data=None)