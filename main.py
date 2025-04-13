import uvicorn
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from database import SessionLocal
import models
from config import HOST, PORT

app = FastAPI()

class Item(BaseModel): # serializer
    id: int
    name: str
    description: str
    price: int
    on_offer: bool

    class Config:
        from_attributes = True

db = SessionLocal()

@app.get('/hello-world', status_code=status.HTTP_200_OK)
def hello_world(name: Optional[str] = "user"):
    return {"message": f"Hello World {name}!"}

@app.get("/items", response_model = List[Item], status_code=status.HTTP_200_OK)
def get_all_items():
    items = db.query(models.Item).all()
    return items

@app.get("/item/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def get_an_item(item_id: int):

    item = db.query(models.Item).filter(models.Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item

@app.post("/item", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_an_item(item: Item):

    new_item = models.Item(
        name=item.name,
        description=item.description,
        price=item.price,
        on_offer=item.on_offer
    )

    db_item = db.query(models.Item).filter(models.Item.name == item.name).first()

    if db_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item already exists")

    db.add(new_item)
    db.commit()
    
    return new_item

@app.put("/item/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def update_an_item(item_id: int, item: Item):
    
    item_to_update = db.query(models.Item).filter(models.Item.id == item_id).first()

    if not item_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    item_to_update.name = item.name
    item_to_update.description = item.description
    item_to_update.price = item.price
    item_to_update.on_offer = item.on_offer

    db.commit()

    return item_to_update

@app.delete("/item/{item_id}")
def delete_an_item(item_id: int):
    
    item_to_delete = db.query(models.Item).filter(models.Item.id == item_id).first()

    if not item_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    db.delete(item_to_delete)
    db.commit()

    return {"message": "Item deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host=HOST,
        port=int(PORT),
        reload=True,
    )


# http://localhost:8000/docs -> Swagger UI
# http://localhost:8000/redoc -> ReDoc UI

# Testing
# @app.get("/")
# def index():
#     return {"message": "Hello, World!"}

# @app.get("/greet/{name}")
# def greet_name(name: str):
#     return {"message": f"Hello, {name}!"}

# @app.get('/greet')
# def greet_optional_name(name: Optional[str] = "user"):
#     return {"message": f"Hello {name}!"}

# @app.put('/item/{item_id}')
# def update_item(item_id: int, item:Item):
#     item_obj = {
#         'name': item.name,
#         'description': item.description,
#         'price': item.price,
#         'on_offer': item.on_offer
#     }

#     return item_obj

