from typing import Optional
from pydantic import BaseModel
from datetime import datetime



class UserRegister(BaseModel):
    email : str
    password : str
    first_name : Optional[str] = None
    last_name : Optional[str] = None

class Machine(BaseModel):
    id : Optional[str] = None
    name : str
    state : Optional[int] = None
    model : Optional[str] = None