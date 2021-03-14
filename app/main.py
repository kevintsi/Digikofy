import uvicorn

from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: Optional[str] = None):
#    return {"item_id": item_id, "q": q}

@app.get("/order")
def get_order() -> int:
    return 1

print(__name__)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)