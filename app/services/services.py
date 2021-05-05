from abc import ABC, abstractmethod
from ..models.models import UserRegister, Machine, PlannedCoffee
from firebase_admin import auth, exceptions
from ..firebase import db
from fastapi.encoders import jsonable_encoder

class UserService(ABC):
    def create_user(self, data : UserRegister):
        try:
            new_user = auth.create_user(
                email= data.email,
                password= data.password
                )
            print(jsonable_encoder(new_user))
            new_user = jsonable_encoder(new_user)
            doc_ref = db.collection('users').document(new_user["_data"]["localId"])
            doc_ref.set({
                'uid' : new_user["_data"]["localId"],
                'email' : new_user["_data"]["email"]
            })
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
            doc_ref = db.collection('machines')
            print(jsonable_encoder(data))
            doc_ref.add(jsonable_encoder(data))
            print("----- End create_machine ----")
            return 201
        except Exception as ex:
            print("Error : {}".format(ex))
            return 401

    def get_machines(self):
        try:
            print("------ Start get machines ------")
            docs = db.collection('machines').stream()
            print("Get machines ---> {}".format(docs))
            machines = []
            for doc in docs:
                machines.append(doc.to_dict())
            print("------ End get machines ------")
            return (200,machines)
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

    def delete_machine(self, id : str):
        try:
            print("----- Start delete_machine -----")
            ref  = db.reference("/Machines")
            ref.child(id).delete()
            print("------ End delete_machine -----")
            return 200
        except Exception as ex:
            print("Error : {}".format(ex))
            return 404

class PlannedCoffeeService(ABC): 
    def create_planned_coffee(self, data : PlannedCoffee):
        try:
            print("------ Start create planned coffee ------")
            ref = db.reference("/PlannedCoffee")
            print(jsonable_encoder(data))
            ref.push(jsonable_encoder(data))
            print("------ End create planned coffee  ------")
            return 201
        except Exception as ex:
            print("Error : {}".format(ex))
            return 401