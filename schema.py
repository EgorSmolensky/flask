from pydantic import BaseModel, EmailStr, validator, ValidationError
import re
from typing import Type, Optional
from errors import HttpException


password_regex = re.compile('((?=.*d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%]).{6,40})')


def check_password(value):
    if not re.search(password_regex, value):
        raise ValueError('Неподходящий пароль')
    return value


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def strong_password(cls, value):
        return check_password(value)


class PatchUserSchema(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]

    @validator("password")
    def strong_password(cls, value):
        return check_password(value)


def validate(data_to_validate: dict, validation_model: Type[CreateUserSchema]):
    try:
        return validation_model(**data_to_validate).dict()
    except ValidationError as er:
        raise HttpException(400, er.errors())
