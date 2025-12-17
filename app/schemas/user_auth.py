from pydantic import EmailStr, BaseModel


class SUserAuth(BaseModel):
    email: EmailStr
    password: str

class SUserRegister(SUserAuth):
    username: str
