import uvicorn
from fastapi import FastAPI, status, Response
from .firebase import *
from .models.models import UserRegister, Machine, PlannedCoffee
from .services.services import UserService, MachineService, PlannedCoffeeService
#from dotenv import load_dotenv


app = FastAPI()
#load_dotenv(dotenv_path=".env")

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


@app.put("/machine", status_code=status.HTTP_200_OK)
async def update_machine(data : Machine, response : Response):
    code = MachineService().update_machine(data)
    if code == 200:
        print("Machine's name update successfully")
    elif code == 404:
        print("Name not found")
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        print("Something went wrong")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

@app.delete("/machine",status_code=status.HTTP_200_OK)
async def delete_machine(id : str, response : Response):
    pass

@app.get("/machine", status_code=status.HTTP_200_OK)
async def get_machines(response : Response):
    (code, data) = MachineService().get_machines()
    print(code)
    if data is not None and code == 200:
        return data
    elif code == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: Optional[str] = None):
#    return {"item_id": item_id, "q": q}

@app.post("/machine", status_code=status.HTTP_201_CREATED)
async def add_machine(data : Machine, response : Response):
    code = MachineService().create_machine(data)
    print(code)
    if code != 201:
        response.status_code = status.HTTP_400_BAD_REQUEST
    
@app.get("/order")
def get_order() -> int:
    return 1


@app.post("/plannedcoffee", status_code=status.HTTP_201_CREATED)
async def add_planned_coffee(data : PlannedCoffee, response : Response):
    code = MachineService().create_machine(data)
    print(code)
    if code != 201:
        response.status_code = status.HTTP_400_BAD_REQUEST


print(__name__)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)