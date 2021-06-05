from abc import ABC, abstractmethod
from ..modules.response_models import CreatePreparation, MachineUpdate, ReportPreparation, UpdatePreparationSaved, UserRegister, Preparation as PreparationResponseModel, Coffee as CoffeeResponseModel, MachineCreate  # , PlannedCoffee
from firebase_admin import auth
from ..modules.models import Coffee, Machine, Preparation, PreparationSaved
from ..firebase import db
from fastapi.encoders import jsonable_encoder
from datetime import date, datetime, timedelta
import pytz

# TODO CHANGE 9KFeGrJB7mQqMVX4RISBGRgI2oJ3 TO DYNAMIC VALUE GET FROM HEADER TOKEN


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
        """
        Create machine

        Args:
            data (MachineCreate): [Data model for creating MachineCreate]

        Returns:
            [Code]: [Status code]
        """
        try:
            print("----- Start create_machine ----")
            users_exist = db.collection('machines').document(
                data.id).collection("users").get()
            print(len(users_exist))
            if len(users_exist) == 0:
                print("Machine never created so no users => creating...")

                db.collection("machines").document(data.id).set({
                    "id": data.id,
                    "state": data.state,
                    "type": data.type
                })

                db.collection("machines").document(data.id).collection("users").document("9KFeGrJB7mQqMVX4RISBGRgI2oJ3").set({
                    "name": data.name,
                    "uid": "9KFeGrJB7mQqMVX4RISBGRgI2oJ3"
                })

            else:
                print("Machine already created so users => adding user...")
                db.collection("machines").document(data.id).collection("users").document("9KFeGrJB7mQqMVX4RISBGRgI2oJ3").set({
                    "name": data.name,
                    "uid": "9KFeGrJB7mQqMVX4RISBGRgI2oJ3"
                })
            print("----- End create_machine ----")
            return 201
        except Exception as ex:
            print("Error : {}".format(ex))
            return 401

    def get_machines(self): #  token : str when I will have the token
        """

        Get all the machines available

        Returns:
            [list(Machine)]: [List of machines]
        """
        try:
            """decode_token = auth.verify_id_token(token)
            uid = decode_token["uid"]
            print("UID : {}".format(uid))"""

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
        """

        Get machine by a given id

        Args:
            id (str): [Machine's id]

        Returns:
            [Machine]: [Machine found]
        """
        try:
            print("------ Start get machine by id ------")
            machine = None
            doc_machine = db.collection(
                'machines').document(id).get().to_dict()
            print(doc_machine)
            doc_machine_user = db.collection("machines").document(id).collection(
                "users").document("9KFeGrJB7mQqMVX4RISBGRgI2oJ3").get()
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
            return 404, machine

    def update_machine(self, id: str, data: MachineUpdate):
        """

        Update machine

        Args:
            id (str): [Id of machine]
            data (MachineUpdate): [data use for updates]

        Returns:
            [Code]: [Status code]
        """
        try:
            print("----- Start update machine's name -----")
            print("{}".format(id))
            db.collection("machines").document(id).collection("users").document(
                "9KFeGrJB7mQqMVX4RISBGRgI2oJ3").update({"name": data.name})
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
    def get_preparation_machine(self, id: str):
        """
        Return all preparations that are programmed for a future time with machine with the given id

        Args:
            id (str): [Id of machine]

        Returns:
            [list]: [Preparations]
        """
        list_preparations = list()
        try:
            print("------ Start get_preparation_machine ------")
            machine_ref = db.collection("machines").document(id)
            print(machine_ref)
            users = db.collection("users").stream()

            for user in users:
                preparations = db.collection("users").document(
                    user.id).collection("preparations").stream()
                print("Docs preparation with id : {} ---> {}".format(id, preparations))

                for preparation in preparations:

                    prepa_dict = preparation.to_dict()
                    nextTime = prepa_dict["nextTime"]
                    year, month, day, hour, minute, second = nextTime.year, nextTime.month, nextTime.day, nextTime.hour, nextTime.minute, nextTime.second

                    date_preparation = datetime(
                        year, month, day, hour, minute, second)
                    print("Early : {}".format(not date_preparation <
                          datetime.now() and prepa_dict["state"] == 0))
                    if not date_preparation < datetime.now() and prepa_dict["state"] == 0:

                        print("Preparation not yet passed")

                        doc_coffee = db.collection("coffees").document(
                            prepa_dict["coffee"].id).get()

                        doc_coffee = doc_coffee.to_dict()

                        coffee = Coffee(id=doc_coffee["id"], name=doc_coffee["name"],
                                        description=doc_coffee["description"])

                        doc_machine = db.collection("machines").document(
                            prepa_dict["machine"].id).get()

                        name = db.collection("machines").document(prepa_dict["machine"].id).collection(
                            "users").document(user.id).get().to_dict()["name"]

                        doc_machine = doc_machine.to_dict()

                        machine = Machine(id=doc_machine["id"], state=doc_machine["state"],
                                          type=doc_machine["type"], name=name)

                        if prepa_dict["saved"]:
                            print("Preparation saved")
                            prep = PreparationSaved(coffee, prepa_dict["creationDate"], prepa_dict["lastUpdate"], machine, 
                            prepa_dict["id"], prepa_dict["saved"], prepa_dict["state"], prepa_dict["nextTime"], prepa_dict["name"],
                             prepa_dict["daysOfWeek"], prepa_dict["hours"], prepa_dict["lastTime"])
                        else:
                            print("Preparation not saved")
                            prep = Preparation(coffee, prepa_dict["creationDate"], prepa_dict["lastUpdate"],
                                                    machine, prepa_dict["id"], prepa_dict["saved"], prepa_dict["state"], prepa_dict["nextTime"])

                        list_preparations.append(prep)

            print("------ End get_preparation_machine ------")
            return 200, list_preparations
        except Exception as ex:
            print("Error : {}".format(ex))
            return 404, list_preparations

    def get_preparation(self):
        preparations = list()
        try:
            print("------ Start get preparation ------")
            docs = db.collection("users").document(
                "9KFeGrJB7mQqMVX4RISBGRgI2oJ3").collection("preparations").stream()
            print("Get Preparation ---> {}".format(docs))
            for doc in docs:
                dico = doc.to_dict()
                print("Coffee reference id --> {}".format(dico["coffee"].id))
                doc_coffee = db.collection("coffees").document(
                    dico["coffee"].id).get()
                coffee = doc_coffee.to_dict()
                print("Information coffee --> {}".format(coffee))
                print(Coffee(id=coffee["id"], name=coffee["name"],
                      description=coffee["description"]))

                coffee = Coffee(id=coffee["id"], name=coffee["name"],
                                description=coffee["description"])

                print("Machine reference id --> {}".format(dico["machine"].id))
                doc_machine = db.collection("machines").document(
                    dico["machine"].id).get()
                machine = doc_machine.to_dict()
                print("Information machine --> {}".format(machine))
                print(Machine(id=machine["id"], state=machine["state"],
                      type=machine["type"]))

                machine = Machine(id=machine["id"], state=machine["state"],
                                  type=machine["type"])

                print(dico)
                if dico["saved"]:
                    print("Preparation saved")
                    preparation = PreparationSaved(coffee, dico["creationDate"], dico["lastUpdate"], machine, 
                    dico["id"], dico["saved"], dico["state"], dico["nextTime"], dico["name"], dico["daysOfWeek"], dico["hours"], dico["lastTime"])
                else:
                    print("Preparation not saved")
                    preparation = Preparation(coffee, dico["creationDate"], dico["lastUpdate"],
                                              machine, dico["id"], dico["saved"], dico["state"], dico["nextTime"])
                preparations.append(preparation)
            print("{}".format(preparations))
            print("------ End get preparation  ------")
            return 200, preparations
        except Exception as ex:
            print("Error : {}".format(ex))
            return 401, preparations

    def report_preparation_started(self, data: ReportPreparation):
        try:
            print("------ Start report_preparation_started ------")

            user = db.collection("users").document(
                "9KFeGrJB7mQqMVX4RISBGRgI2oJ3")

            prep = user.collection("preparations").document(
                data.preparation_id)

            print(prep)
            prep.update({"state": 1})

            machine_id = prep.get().to_dict()["machine"].id
            print(machine_id)

            db.collection("machines").document(machine_id).update({"state": 1})

            notif_ref = user.collection("notifications").document()

            notif_ref.set({
                "id": notif_ref.id,
                "preparation": prep,
                "state": 0
            })

            print("------ End report_preparation_started ------")

            return 200
        except Exception as ex:
            print("Error : {}".format(ex))
            return 404

    def report_preparation_succeeded(self, data: ReportPreparation):
        try:
            print("------ Start report_preparation_succeeded ------")

            user = db.collection("users").document(
                "9KFeGrJB7mQqMVX4RISBGRgI2oJ3")

            prep = user.collection("preparations").document(
                data.preparation_id)

            print(prep)
            prep.update({"state": 0})

            machine_id = prep.get().to_dict()["machine"].id
            print(machine_id)

            db.collection("machines").document(machine_id).update({"state": 0})

            prep_dict = prep.get().to_dict()

            is_saved = prep_dict["saved"]

            if is_saved:

                next_time = calculate_next_time(prep_dict["daysOfWeek"], prep_dict["hours"], prep_dict["nextTime"])

                print("New value of next_time = {}".format(next_time))

                prep.update({
                    "lastTime": prep_dict["nextTime"],
                    "nextTime": next_time
                })
            

            notif_ref = user.collection("notifications").document()

            notif_ref.set({
                "id": notif_ref.id,
                "preparation": prep,
                "state": 1
            })

            print("------ End report_preparation_succeeded ------")

            return 200
        except Exception as ex:
            print("Error : {}".format(ex))
            return 404

    def report_preparation_failed(self, data: ReportPreparation):
        try:
            print("------ Start report_preparation_failed ------")

            user = db.collection("users").document(
                "9KFeGrJB7mQqMVX4RISBGRgI2oJ3")

            prep = user.collection("preparations").document(
                data.preparation_id)

            print(prep)
            prep.update({"state": 0})

            machine_id = prep.get().to_dict()["machine"].id
            print(machine_id)

            db.collection("machines").document(machine_id).update({"state": 0})

            prep_dict = prep.get().to_dict()

            is_saved = prep_dict["saved"]

            if is_saved:
                
                next_time = calculate_next_time(prep_dict["daysOfWeek"], prep_dict["hours"], prep_dict["nextTime"])
                prep.update({
                    "lastTime": prep_dict["nextTime"],
                    "nextTime": next_time
                })
            else:
                # TODO what happen
                pass

            notif_ref = user.collection("notifications").document()

            notif_ref.set({
                "id": notif_ref.id,
                "preparation": prep,
                "state": 2
            })

            print("------ End report_preparation_failed ------")

            return 200
        except Exception as ex:
            print("Error : {}".format(ex))
            return 404

    def create_preparation(self, data: CreatePreparation):
        try:
            print("------- Start create_preparation -------")
            prep = db.collection("users").document(
                "9KFeGrJB7mQqMVX4RISBGRgI2oJ3").collection("preparations").document()

            coffee = db.collection("coffees").document(data.coffee_id)
            machine = db.collection("machines").document(data.machine_id)
            
            prep_dict = prep.get().to_dict()

            if data.saved:

                next_time = calculate_next_time(data.days_of_week, data.hours, prep_dict["nextTime"])

                prep.set({
                    "coffee": coffee,
                    "creationDate": datetime.now(tz=pytz.utc),
                    "daysOfWeek": data.days_of_week,
                    "hours": data.hours,
                    "id": prep.id,
                    "lastTime": datetime.now(tz=pytz.utc),
                    "lastUpdate": datetime.now(tz=pytz.utc),
                    "machine": machine,
                    "name": data.name,
                    "saved": data.saved,
                    "nextTime" : next_time,
                    "state" : 0
                })
            else:
                prep.set({
                    "coffee": coffee,
                    "creationDate": datetime.now(tz=pytz.utc),
                    "id": prep.id,
                    "lastUpdate": datetime.now(tz=pytz.utc),
                    "machine": machine,
                    "nextTime" : datetime.strptime(data.next_time, "%Y-%m-%dT%H:%M:%SZ"),
                    "saved": data.saved,
                    "state" : 0
                })
            print("------- End create_preparation -------")
            return 201
        except Exception as ex:
            print("Error : {}".format(ex))
            return 404

    def update_preparation(self, data : UpdatePreparationSaved, id : str):
        try:
            print("------ Start update_preparation ------")

            prepa = db.collection('users').document("9KFeGrJB7mQqMVX4RISBGRgI2oJ3").collection("preparations").document(id)
            
            coffee = db.collection('coffees').document(data.coffee_id)

            machine = db.collection('machines').document(data.machine_id)

            next_time = calculate_next_time(data.days_of_week, data.hours, prepa.get().to_dict()["nextTime"])

            print("Date now  = {} {} and date nexttime =  {} {}".format(datetime.now(tz=pytz.utc), type(datetime.now(tz=pytz.utc)), next_time, type(next_time)))

            prepa.update({"name" : data.name,
             "lastUpdate" : datetime.now(tz=pytz.utc),
             "daysOfWeek" : data.days_of_week,
             "hours" : data.hours,
             "nextTime" : next_time,
             "coffee" : coffee,
             "machine" : machine
             })

            print("------ End update_preparation ------")
            return 200
        except Exception as ex:
            print("Error : {}".format(ex))
            return 400

    def delete_preparation(self, id : str):
        try:
            print("------ Start delete_preparation ------")
            prepa = db.collection('users').document("9KFeGrJB7mQqMVX4RISBGRgI2oJ3").collection("preparations").document(id)
            prepa.delete()
            print("------ End delete_preparation ------")
            return 200
        except Exception as ex:
            print("Error : {}".format(ex))
            return 400


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



def calculate_next_time(day_of_week : list, hours : list, old_next_time):

    print("---- Start calculate_next_time ------")
    
    current_date = datetime.now(tz=pytz.utc)

    current_dayofweek = current_date.weekday()  # day = 6
    # daysOfWeek = [4,5,6]

    if len(day_of_week) > 1:
        i = 0
        
        while current_dayofweek > day_of_week[i]:
            i = i+1

        if i == len(day_of_week) - 1:
            index_wanted_found = 0
        else:
            index_wanted_found = i

        print("Index the closest day of week : {0} so prep_dict[{0}] = {1}".format(
            index_wanted_found, day_of_week[index_wanted_found]))

        next_time = current_date

        while day_of_week[index_wanted_found] != next_time.weekday()+1:
            print("Next time : {} and weekdays : {}".format(
                next_time, next_time.weekday()))
            next_time = next_time + timedelta(days=1)

        print("Next date : {}".format(next_time))

    else:
        next_time = current_date + \
            timedelta(days=day_of_week[0]-1)
        print("Next date : {}".format(next_time))

    has_same_date = ((old_next_time.day == current_date.day) and (
        old_next_time.month == current_date.month) and (old_next_time.year == current_date.year))
    
    print(has_same_date)
    if not has_same_date:
        print("Not the same date")
        splitted_hours = hours[0].split(":")
        hour = int(splitted_hours[0])
        minute = int(splitted_hours[1])
        second = int(splitted_hours[2])

        print("Hour = {} , Minute = {} , Second = {}".format(
            hour, minute, second))

        next_time = datetime(
            next_time.year, next_time.month, next_time.day, hour, minute, second, 0, tzinfo=pytz.utc)

        print("Next time with hour = {}".format(next_time))
    else:
        print("Same date")
        i = 0
        for h in hours:
            splitted_hours = h.split(":")
            hour = int(splitted_hours[0])
            minute = int(splitted_hours[1])
            second = int(splitted_hours[2])

            new_date = current_date.replace(
                hour=hour, minute=minute, second=second, microsecond=0, tzinfo=pytz.utc)

            if new_date > current_date:
                next_time = new_date
                break

        print("Next time with hour = {}".format(next_time))

    return next_time
