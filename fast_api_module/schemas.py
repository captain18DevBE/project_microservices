from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    id: str
    full_name: str
    phone_number: str
    email: str
    balance: float

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str
    transactions: List["Transaction"] = []

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    amount: float


class TransactionCreate(TransactionBase):
    owner_id: str
    fee_id: Optional[int]


class TransactionUpdate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    owner_id: str
    fee_id: Optional[int]

    class Config:
        orm_mode = True

class FeeBase(BaseModel):
    student_id: str
    student_name: str
    fee_type: str
    amount_due: float

class FeeCreate(FeeBase):
    pass

class Fee(FeeBase):
    id: int
    transactions: List[Transaction] = []

    class Config:
        orm_mode = True

class AccountBase(BaseModel):
    username: str
    password: str

class AccountCreate(AccountBase):
    user_id: str

class Account(AccountBase):
    id: int
    user: Optional[User] = None

    class Config:
        orm_mode = True

class OTPBase(BaseModel):
    otp: str
    expiry: datetime
    user_id: str

class OTPCreate(OTPBase):
    pass

class OTP(OTPBase):
    id: int

    class Config:
        orm_mode = True
