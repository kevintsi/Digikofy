from os import name
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserRegister(BaseModel):
    email: str
    password: str


class MachineUpdate(BaseModel):
    name: str

class MachineCreate(BaseModel):
    id : str
    state : Optional[int] = None
    type : Optional[int] = None
    name : str


class ReportPreparation(BaseModel):
    preparation_id : str



class Coffee(BaseModel):
    id: Optional[str] = None
    name: str
    description: str



class CreatePreparation(BaseModel):
    coffee_id: str
    days_of_week : Optional[list] = None
    hours : Optional[list] = None
    machine_id : str
    name : str
    saved : bool
    state : int

class UpdatePreparation(BaseModel):
    name : str


class Preparation(BaseModel):
    id: Optional[str] = None
    coffee: Coffee
    next_time: datetime
    saved: bool
    last_time: Optional[datetime] = None
    name: Optional[str] = None
    daysOfWeek: Optional[list] = None
    hours: Optional[list] = None
    creation_date: datetime = None
    last_update: datetime = None
