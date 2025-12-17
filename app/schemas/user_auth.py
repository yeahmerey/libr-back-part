from pydantic import EmailStr, BaseModel


class SUserAuth(BaseModel):
    username: str
    password: str

class SUserRegister(SUserAuth):
    username: str
