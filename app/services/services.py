from abc import ABC, abstractmethod
from ..models.models import UserRegister
from firebase_admin import auth

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