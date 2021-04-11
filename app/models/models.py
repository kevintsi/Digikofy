from typing import Optional
from pydantic import BaseModel


class UserRegister(BaseModel):
    email : str
    password : str
    first_name : str
    last_name : str