import datetime as _dt

import pydantic as _pydantic

from pydantic import BaseModel, EmailStr


class _UserBase(BaseModel):
    email: EmailStr


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(_UserBase):
    id: int

    class Config:
        orm_mode = True


class _LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    company: str
    note: str


class Lead(_LeadBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
    last_updated: _dt.datetime
