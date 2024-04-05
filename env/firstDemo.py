from fastapi import FastAPI, Query
from enum import Enum
from pydantic import BaseModel

app = FastAPI()

@app.get("/", description="This is our first app with fastapi")
async def base_get_route():
    return {"message": "welcome to fastapi"}

@app.post("/")
async def post():
    return {"message": "hello from the post route"}

@app.put("/")
async def put():
    return {"message": "hello from the put route"}

@app.get("/users")
async def list_users():
    return {"message": "list users route"}

@app.get("/users/me")
async def get_current_user():
    return {"message": "this is the current user"}

@app.get("/users/{user_id}")
async def get_user_by_id(user_id:str):
    return{"user id": user_id}

class FoodEnum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"

@app.get("/foods/{food_name}")
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {"food name": food_name,
                "message": "you're healthy"}
    if food_name.value == "fruits":
        return {"food nam": food_name,
                "message": "you're still healthy"}
    return {"food name": food_name, "message": "i like chocalate!"}

#Query parameters
fake_item_db = [{"item_name": "item1"}, {"item_name": "item2"}, {"item_name": "item3"}]

@app.get("/items")
async def list_items(skip: int=0, limit: int=10):
    return fake_item_db[skip: skip + limit]

@app.get("/items/{item_id}")
async def get_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update({"description": "bla bla"})
    return item

#Request Body

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None =     None

@app.post("/items")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def create_item_with_put(item_id : int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

#Query parameters and String validation

@app.get("/items")
async def read_items_list(q: str | None = Query(None, max_length=10)):
    results = {"items": [{"item_id": "foo"}, {"item_id": "whatever"}]}
    if q:
        results.update({"q": q})
    return results