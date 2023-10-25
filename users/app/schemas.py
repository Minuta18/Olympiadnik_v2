from pydantic import BaseModel

class VerifyPasswordSchema(BaseModel):
    username: str|None = None
    email: str|None = None
    phone: str|None = None
    password: str

class CreateUserSchema(BaseModel):
    email: str
    phone: str|None = None

    username: str
    first_name: str|None = None
    last_name: str|None = None
    middle_name: str|None = None

    password: str
