from typing import Optional
from pydantic import BaseModel
from datetime import datetime



class UserRegister(BaseModel):
    email : str
    password : str
    first_name : str
    last_name : str

class Machine(BaseModel):
    id : Optional[str] = None
    name : str
    state : int
    model : str