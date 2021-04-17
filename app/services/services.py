from abc import ABC, abstractmethod
from ..models.models import UserRegister, Machine
from firebase_admin import auth, db, exceptions
from fastapi.encoders import jsonable_encoder

class UserService(ABC):
    def create_user(self, data : UserRegister):
        try:
            auth.create_user(
                email= data.email,
                password= data.password,
                display_name= "{} {}".format(data.first_name, data.last_name))
            return 201 
        except auth.EmailAlreadyExistsError as ex: 
            print(type(ex))
            return 409
        except Exception as ex:
            return 500

    def log_in_user(self, data):
        pass


class MachineService(ABC):
    def create_machine(self, data : Machine):
        try:
            print("----- Start create_machine ----")
            ref = db.reference("/Machines")
            print(jsonable_encoder(data))
            ref.push(jsonable_encoder(data))
            print("----- End create_machine ----")
            return 201
        except Exception as ex:
            print("Error : {}".format(ex))
            return 401

    def get_machines(self):
        pass    