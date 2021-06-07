from typing import Any, List
import uvicorn
from fastapi import FastAPI, status, Response, Request
from .modules.response_models import CreatePreparation, MachineCreate, ReportPreparation, \
    UpdatePreparationSaved, UserRegister, MachineUpdate, Machine, Coffee
from .modules.services import UserService, MachineService, PreparationService, CoffeeService


app = FastAPI(title="DigikofyAPI")

###### USER REGISTERY ROUTE ########

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: UserRegister, response: Response):
    code = UserService().create_user(data)
    if code == 201:
        print('Sucessfully created new user')
    elif code == 409:
        print("An user with this email address already exists")
        response.status_code = status.HTTP_409_CONFLICT
    else:
        print("Something went wrong")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

###### MACHINE'S ROUTE ############


@app.post("/machine", status_code=status.HTTP_201_CREATED)
async def add_machine(data: MachineCreate, response: Response):
    code = MachineService().create_machine(data)
    print(code)
    if code != 201:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@app.get("/machines", status_code=status.HTTP_200_OK, response_model=List[Machine])
async def get_machines(response: Response, request : Request):
    print(request.headers)
    """token = check_auth(request)
    if token == "":
        response.status_code = status.HTTP_403_FORBIDDEN
        return"""

    (code, data) = MachineService().get_machines()
    print(code)
    if code == 200:
        return data
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

@app.get("/machine/{id}", status_code=status.HTTP_200_OK, response_model=Machine)
async def get_machines(id: str, response: Response):
    (code, data) = MachineService().get_machine_by_id(id)
    print(code)
    if code == 200:
        return data
    elif code == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@app.put("/machine/{id}", status_code=status.HTTP_200_OK)
async def update_machine(id: str, data : MachineUpdate, response: Response):
    code = MachineService().update_machine(id, data)
    if code == 200:
        print("Machine's name update successfully")
    else:
        print("Name not found")
        response.status_code = status.HTTP_404_NOT_FOUND


@app.delete("/machine/{id}", status_code=status.HTTP_200_OK)
async def delete_machine(id: str, response: Response):
    code = MachineService().delete_machine(id)
    if code != 200 and code != 500:
        response.status_code = status.HTTP_404_NOT_FOUND
    elif code == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


######## COFFEE'S ROUTE ##########


@app.get("/coffees", status_code=status.HTTP_200_OK, response_model=List[Coffee])
async def get_coffee(response: Response):
    (code, data) = CoffeeService().get_coffee()
    print(code)
    if code == 200:
        return data
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@app.get("/coffee/{id}", status_code=status.HTTP_200_OK, response_model=Coffee)
async def get_coffee_by_id(id: str, response: Response):
    (code, data) = CoffeeService().get_coffee_by_id(id)
    print(code, data)
    if code == 200:
        return data
    elif code == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


###### PREPARATION'S ROUTE ##########

@app.post("/preparation", status_code=status.HTTP_201_CREATED)
async def add_preparation(data: CreatePreparation, response: Response):
    code = PreparationService().create_preparation(data)
    print(code)
    if code != 201 and code != 500:
        response.status_code = status.HTTP_404_NOT_FOUND
    elif code == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

@app.get("/preparations", status_code=status.HTTP_200_OK)
async def get_preparation(response: Response):
    code, preparations = PreparationService().get_preparation()
    if code == 200:
        return preparations
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@app.put("/preparation/{id}", status_code=status.HTTP_200_OK)
async def update_preparation(id : str, data: UpdatePreparationSaved, response: Response):
    code = PreparationService().update_preparation(data, id)
    print(code)
    if code != 200 and code != 500:
        response.status_code = status.HTTP_404_NOT_FOUND
    elif code == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@app.delete("/preparation/{id}", status_code=status.HTTP_200_OK)
async def delete_preparation(id : str, response: Response):
    code = PreparationService().delete_preparation(id)
    print(code)
    if code != 200 and code != 500:
        response.status_code = status.HTTP_404_NOT_FOUND
    elif code == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

####### PREPARATION MACHINE'S ROUTE ##########

@app.post("/preparation/started", status_code=status.HTTP_200_OK)
async def report_preparation_started(data: ReportPreparation, response: Response):
    code = PreparationService().report_preparation_started(data)
    print(code)
    if code != 200 and code != 500:
        response.status_code = status.HTTP_400_BAD_REQUEST
    elif code == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

@app.post("/preparation/succeeded", status_code=status.HTTP_200_OK)
async def report_preparation_succeeded(data: ReportPreparation, response: Response):
    code = PreparationService().report_preparation_succeeded(data)
    print(code)
    if code != 200 and code != 500:
        response.status_code = status.HTTP_400_BAD_REQUEST
    elif code == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@app.post("/preparation/failed", status_code=status.HTTP_200_OK)
async def report_preparation_failed(data: ReportPreparation, response: Response):
    code = PreparationService().report_preparation_failed(data)
    print(code)
    if code != 200 and code != 500:
        response.status_code = status.HTTP_400_BAD_REQUEST
    elif code == 500:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

@app.get("/preparation/machine/{id}", status_code=status.HTTP_200_OK, response_model=List[Any])
async def get_preparation_machine(id: str, response: Response):
    code, preparations = PreparationService().get_preparation_machine(id)
    if code == 200:
        return preparations
    elif code == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

@app.get("/preparation/nextcoffee/{id}", status_code=status.HTTP_200_OK, response_model=List[Any])
async def get_preparation_next_coffee(id: str, response: Response):
    """
    Route that returns late coffees to be prepared 

    Args:
        id (str): [Machine's id]
        response (Response): [Response]

    Returns:
        [type]: [description]
    """
    code, preparations = PreparationService().get_preparation_next_coffe(id)
    if code == 200:
        return preparations
    elif code == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


###### OTHER FUNCTIONS #######

def check_auth(request : Request):
    token = ""
    if "Authorization" not in request.headers:
        return token
    else:
        token = request.headers["Authorization"].split(" ")[1]
        return token

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
