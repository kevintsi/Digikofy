import uvicorn
from fastapi import FastAPI, status, Response
from .modules.response_models import CreatePreparation, MachineCreate, ReportPreparation, UserRegister, MachineUpdate, Preparation
from .modules.services import UserService, MachineService, PreparationService, CoffeeService
#from dotenv import load_dotenv


app = FastAPI()
# load_dotenv(dotenv_path=".env")


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



@app.put("/machine/{id}", response_model=MachineUpdate, status_code=status.HTTP_200_OK)
async def update_machine(id: str, data : MachineUpdate, response: Response):
    code = MachineService().update_machine(id, data)
    if code == 200:
        print("Machine's name update successfully")
    elif code == 404:
        print("Name not found")
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        print("Something went wrong")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@app.delete("/machine", status_code=status.HTTP_200_OK)
async def delete_machine(id: str, response: Response):
    code = MachineService().delete_machine(id)
    if code != 200:
        response.status_code = status.HTTP_403_FORBIDDEN


@app.get("/machine", status_code=status.HTTP_200_OK)
async def get_machines(response: Response):
    (code, data) = MachineService().get_machines()
    print(code)
    if data is not None and code == 200:
        return data
    elif code == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

@app.get("/machine/{id}", status_code=status.HTTP_200_OK)
async def get_machines(id: str, response: Response):
    (code, data) = MachineService().get_machine_by_id(id)
    print(code)
    if data is not None and code == 200:
        return data
    elif code == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR



@app.post("/machine", status_code=status.HTTP_201_CREATED)
async def add_machine(data: MachineCreate, response: Response):
    code = MachineService().create_machine(data)
    print(code)
    if code != 201:
        response.status_code = status.HTTP_400_BAD_REQUEST


@app.get("/coffee", status_code=status.HTTP_201_CREATED)
async def get_coffee(response: Response):
    (code, data) = CoffeeService().get_coffee()
    print(code)
    if data is not None and code == 200:
        return data
    elif code == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@app.get("/coffee/{id}", status_code=status.HTTP_201_CREATED)
async def get_coffee_by_id(id: str, response: Response):
    (code, data) = CoffeeService().get_coffee_by_id(id)
    print(code, data)
    if data is not None and code == 200:
        return data
    elif code == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR



@app.post("/preparation", status_code=status.HTTP_201_CREATED)
async def add_preparation(data: CreatePreparation, response: Response):
    code = PreparationService().create_preparation(data)
    print(code)
    if code != 201:
        response.status_code = status.HTTP_400_BAD_REQUEST

@app.get("/preparation", status_code=status.HTTP_200_OK)
async def get_preparation(response: Response):
    code, preparations = PreparationService().get_preparation()
    if code == 200 and len(preparations) > 0:
        return preparations
    else:
        response.status_code = status.HTTP_404_NOT_FOUND


@app.get("/preparation/machine/{id}", status_code=status.HTTP_200_OK)
async def get_preparation_machine(id: str, response: Response):
    code, preparations = PreparationService().get_preparation_machine(id)
    if code == 200 and len(preparations) > 0:
        return preparations
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

@app.post("/preparation/started", status_code=status.HTTP_200_OK)
async def report_preparation_started(data: ReportPreparation, response: Response):
    code = PreparationService().report_preparation_started(data)
    print(code)
    if code != 200:
        response.status_code = status.HTTP_400_BAD_REQUEST

@app.post("/preparation/succeeded", status_code=status.HTTP_200_OK)
async def report_preparation_succeeded(data: ReportPreparation, response: Response):
    code = PreparationService().report_preparation_succeeded(data)
    print(code)
    if code != 200:
        response.status_code = status.HTTP_400_BAD_REQUEST


@app.post("/preparation/failed", status_code=status.HTTP_200_OK)
async def report_preparation_failed(data: ReportPreparation, response: Response):
    code = PreparationService().report_preparation_failed(data)
    print(code)
    if code != 200:
        response.status_code = status.HTTP_400_BAD_REQUEST



print(__name__)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
