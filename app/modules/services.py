from abc import ABC, abstractmethod
from ..modules.responseModels import MachineUpdate, UserRegister, Preparation, Coffee as CoffeeResponseModel, MachineCreate  # , PlannedCoffee
from firebase_admin import auth, exceptions
from ..modules.models import Coffee, Machine
from ..firebase import db
from fastapi.encoders import jsonable_encoder


class UserService(ABC):
    def create_user(self, data: UserRegister):
        try:
            new_user = auth.create_user(
                email=data.email,
                password=data.password
            )
            print(jsonable_encoder(new_user))
            new_user = jsonable_encoder(new_user)
            doc_ref = db.collection('users').document(
                new_user["_data"]["localId"])
            doc_ref.set({
                'uid': new_user["_data"]["localId"],
                'email': new_user["_data"]["email"]
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
    def create_machine(self, data: MachineCreate):
        try:
            print("----- Start create_machine ----")
            users_exist = db.collection('machines').document(data.id).collection("users").get()
            print(len(users_exist))
            if len(users_exist) == 0:
                print("Machine never created so no users => creating...")

                db.collection("machines").document(data.id).set({
                    "id" : data.id,
                    "state" : data.state,
                    "type" : data.type
                })

                db.collection("machines").document(data.id).collection("users").document("9KFeGrJB7mQqMVX4RISBGRgI2oJ3").set({
                    "name" : data.name,
                    "uid" : "9KFeGrJB7mQqMVX4RISBGRgI2oJ3"
                })

            else:
                print("Machine already created so users => adding user...")
                db.collection("machines").document(data.id).collection("users").document("sddsdsd").set({
                    "name" : data.name,
                    "uid" : "dsdsdsds"
                })
            print("----- End create_machine ----")
            return 201
        except Exception as ex:
            print("Error : {}".format(ex))
            return 401

    def get_machines(self):
        try:
            print("------ Start get machines ------")
            machines = []
            doc_machines = db.collection('machines').stream()
            for doc in doc_machines:
                dico_machine = doc.to_dict()
                print(dico_machine)
                docs_user_machine = db.collection('machines').document(dico_machine["id"]).collection(
                    "users").where("uid", "==", "9KFeGrJB7mQqMVX4RISBGRgI2oJ3").stream()
                print("Get machines ---> {}".format(docs_user_machine))
                for doc_mach_user in docs_user_machine:
                    dico_machine_user = doc_mach_user.to_dict()
                    print("User's machine info : {}".format(dico_machine_user))
                    machines.append(Machine(
                        id=dico_machine["id"], name=dico_machine_user["name"], state=dico_machine["state"], type=dico_machine["type"]))
            print(machines)
            print("------ End get machines ------")
            return 200, machines
        except Exception as ex:
            print("Error : {}".format(ex))
            return 404, []

    def get_machine_by_id(self, id: str):
        try:
            print("------ Start get machine by id ------")
            machine = None
            doc_machine = db.collection(
                'machines').document(id).get().to_dict()
            print(doc_machine)
            doc_machine_user = db.collection("machines").document(id).collection("users").document("9KFeGrJB7mQqMVX4RISBGRgI2oJ3").get()
            print(doc_machine_user)
            dico_machine_user = doc_machine_user.to_dict()
            print(dico_machine_user)
            print("User's machine info : {}".format(dico_machine_user))
            machine = Machine(id=doc_machine["id"], name=dico_machine_user["name"],
                                state=doc_machine["state"], type=doc_machine["type"])
            print(machine)
            print("------ End get machines ------")
            return 200, machine
        except Exception as ex:
            print("Error : {}".format(ex))
            return 404, []

    def update_machine(self, id: str, data : MachineUpdate):
        try:
            print("----- Start update machine's name -----")
            print("{}".format(id))
            db.collection("machines").document(id).collection("users").document("9KFeGrJB7mQqMVX4RISBGRgI2oJ3").update({"name" : data.name })
            print("------ End update machine's name -----")
            return 200
        except Exception as ex:
            print("Error : {}".format(ex))
            return 404

    def delete_machine(self, id: str):
        try:
            print("----- Start delete_machine -----")
            db.collection("machines").document(id).delete()
            print("------ End delete_machine -----")
            return 200
        except Exception as ex:
            print("Error : {}".format(ex))
            return 404


class PreparationService(ABC):
    # def create_preparation(self, data : Preparation):
    # try:
    #print("------ Start create preparation ------")
    #doc_ref = db.collection("/preparations")
    # if data.last_
    # print(jsonable_encoder(data))
    # ref.push(jsonable_encoder(data))
    #print("------ End create preparation  ------")
    # return 201
    # except Exception as ex:
    #print("Error : {}".format(ex))
    # return 401

    def get_preparation(self):
        try:
            print("------ Start get preparation ------")
            docs = db.collection(
                'users/9KFeGrJB7mQqMVX4RISBGRgI2oJ3/preparations').stream()
            print("Get Preparation ---> {}".format(docs))
            preparations = list()
            for doc in docs:
                dico = doc.to_dict()
                print("Coffee reference id --> {}".format(dico["coffee"].id))
                doc_coffee = db.collection("coffees").document(
                    dico["coffee"].id).get()
                coffee = doc_coffee.to_dict()
                print("Information coffee --> {}".format(coffee))
                print(Coffee(id=coffee["id"], name=coffee["name"],
                      description=coffee["description"]).__str__())
                # preparations.append(doc.to_dict())
            print("{}".format(preparations))
            print("------ End get preparation  ------")
        except Exception as ex:
            print("Error : {}".format(ex))
            return 401


class CoffeeService(ABC):
    def get_coffee(self):
        try:
            print("------ Start get_coffee ------")
            docs = db.collection('coffees').stream()
            print("Get coffees ---> {}".format(docs))
            coffees = []
            for doc in docs:
                coffees.append(doc.to_dict())
            print("------ End get_coffee ------")
            return (200, coffees)
        except Exception as ex:
            print("Error : {}".format(ex))
            return 404

    def get_coffee_by_id(self, id):
        try:
            print("----- Start get_coffee_by_id ----")
            doc = db.collection('coffees').document(id).get()
            print("----- End get_coffee_by_id ----")
            return (200, doc.to_dict())
        except Exception as ex:
            print("Error : {}".format(ex))
            return 401
