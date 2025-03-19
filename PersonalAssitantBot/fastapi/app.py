from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def hello():
    return {"message": "Hello, World!"}


@app.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id, "name": "item"}  # return the item name based