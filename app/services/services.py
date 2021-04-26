from abc import ABC, abstractmethod
from ..models.models import UserRegister, Machine
from firebase_admin import auth, db, exceptions
from fastapi.encoders import jsonable_encoder

class UserService(ABC):
    def create_user(self, data : UserRegister):
        try:
            auth.create_user(
                email= data.email,
                password= data.password
                )
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
        try:
            print("------ Start get machines ------")
            ref = db.reference("/Machines")
            print("------ End get machines ------")
            return (200,ref.get())
        except Exception as ex:
            print("Error : {}".format(ex))
            return 404

    def update_machine(self, data : Machine):
        try:
            print("----- Start update machine's name -----")
            print("{}".format(data))
            ref  = db.reference("/Machines")
            ref.child(data.id).update({"name" : data.name})
            print("------ End update machine's name -----")
            return 200
        except Exception as ex:
            print("Error : {}".format(ex))
            return 404
