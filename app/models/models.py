from typing import Optional
from pydantic import BaseModel
from datetime import datetime



class UserRegister(BaseModel):
    email : str
    password : str

class Machine(BaseModel):
    id : Optional[str] = None
    name : str
    state : Optional[int] = None
    model : Optional[str] = None

class PlannedCoffee(BaseModel):
    id : Optional[str] = None
    name : str
    moments : datetime
    coffe_id : str
    user_id : str
    machine_id : str

class Coffee(BaseModel):
    id : Optional[str] = None
    name : str
    description : str


class Preparation(BaseModel):
    id : Optional[str] = None
    moment : datetime
    coffee_id : str
    user_id : str
    machine_id : str
