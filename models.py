from pydantic import BaseModel, EmailStr


class Todo(BaseModel):
    name: str
    discription: str



# -------- Users ----------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr

#-------------- for send otp ----------
class EmailSchema(BaseModel):
    email: EmailStr

class VerifyOTPSchema(BaseModel):
    email: EmailStr
    otp: str