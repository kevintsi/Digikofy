import uvicorn
<<<<<<< HEAD

from typing import Optional

from fastapi import FastAPI

app = FastAPI()

=======
from fastapi import FastAPI, status, Response
from .firebase import *
from .models.models import UserRegister
from .services.services import UserService
#from dotenv import load_dotenv


app = FastAPI()
#load_dotenv(dotenv_path=".env")
>>>>>>> c88763c0ce94aa18d55f82203aa3c9c353cd776a

@app.get("/")
def read_root():
    return {"Hello": "World"}


<<<<<<< HEAD
=======
@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data : UserRegister, response  : Response):
    code = UserService().create_user(data)
    if code == 201: 
        print('Sucessfully created new user')
    elif code == 409:
        print("An user with this email address already exists")
        response.status_code = status.HTTP_409_CONFLICT
    else:
        print("Something went wrong")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


>>>>>>> c88763c0ce94aa18d55f82203aa3c9c353cd776a
#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: Optional[str] = None):
#    return {"item_id": item_id, "q": q}

@app.get("/order")
def get_order() -> int:
    return 1

print(__name__)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)