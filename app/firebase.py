import firebase_admin
from firebase_admin import credentials
import os

data = os.path.abspath(os.path.dirname(__file__)) + "/private_key_sdk_digikofy.json"
cred = credentials.Certificate(data)
firebase_admin.initialize_app(cred)