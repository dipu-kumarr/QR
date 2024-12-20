from pydantic import BaseModel, constr

class UserBase(BaseModel):
    name: str
    age: int
    address: str
    mobile: constr(regex=r'^\d{10}$')  # Validate 10-digit mobile number

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
