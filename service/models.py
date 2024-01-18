from typing import Optional, List

from pydantic import BaseModel, Field


class WriteDataModel(BaseModel):
    phone: str = Field(pattern=r"^8[0-9]{10}$")
    address: str


class CheckDataModel(BaseModel):
    phone: str = Field(pattern=r"^8[0-9]{10}$")


class ValidationError(BaseModel):
    field: str
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: Optional[str]
    validation_error: Optional[List[ValidationError]]
    debug: Optional[str]


class Result(BaseModel):
    result: str