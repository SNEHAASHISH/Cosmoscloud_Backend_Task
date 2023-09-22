from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB configurations
MONGODB_URL = "mongodb+srv://admin:admin@cluster0.aymt9br.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "ecommerce"  # Change this to your actual database name if different

client = AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]

class Product(BaseModel):
    id: int
    name: str
    price: float
    available_quantity: int


class UserAddress(BaseModel):
    city: str
    country: str
    zip_code: str


class OrderItem(BaseModel):
    product_id: int
    bought_quantity: int


class Order(BaseModel):
    timestamp: str
    items: List[OrderItem]
    total_amount: float
    user_address: UserAddress


app = FastAPI()

# Mock database
products_db = [
    {"id": 1, "name": "TV", "price": 500.0, "available_quantity": 10},
    {"id": 2, "name": "AC", "price": 400.0, "available_quantity": 10},
    {"id": 3, "name": "Fridge", "price": 450.0, "available_quantity": 10},
    {"id": 4, "name": "Powerbank", "price": 50.0, "available_quantity": 10},
    {"id": 5, "name": "Tablet", "price": 200.0, "available_quantity": 10},
    {"id": 6, "name": "Laptop", "price": 600.0, "available_quantity": 10},
    {"id": 7, "name": "AirPods", "price": 200.0, "available_quantity": 10},
    {"id": 8, "name": "AirPods Pro", "price": 300.0, "available_quantity": 10},
    {"id": 9, "name": "Mobile", "price": 800.0, "available_quantity": 10},
    {"id": 10, "name": "Washing Machine", "price": 700.0, "available_quantity": 10},
    {"id": 11, "name": "Sewing Machine", "price": 150.0, "available_quantity": 10},
    {"id": 12, "name": "Hair Dryer", "price": 100.0, "available_quantity": 10},
    {"id": 13, "name": "Toaster", "price": 50.0, "available_quantity": 10},
    {"id": 14, "name": "OTG", "price": 200.0, "available_quantity": 10},
    {"id": 15, "name": "Fan", "price": 350.0, "available_quantity": 10}
]

orders_db = []


@app.on_event("startup")
async def startup_event():
    app.mongodb_client = client
    app.mongodb = db


@app.on_event("shutdown")
async def shutdown_event():
    app.mongodb_client.close()


@app.get("/")
async def read_root():
    return {"message": "Welcome to the E-commerce API!"}


@app.get("/products/")
async def list_products():
    return products_db


@app.post("/orders/")
async def create_order(order: Order):
    total_amount = 0
    for item in order.items:
        product = next((p for p in products_db if p["id"] == item.product_id), None)
        if not product or product["available_quantity"] < item.bought_quantity:
            raise HTTPException(status_code=400, detail="Product not available in desired quantity")
        total_amount += product["price"] * item.bought_quantity
        product["available_quantity"] -= item.bought_quantity

    if total_amount != order.total_amount:
        raise HTTPException(status_code=400, detail="Total amount mismatch")

    order_id = len(orders_db) + 1
    order_dict = order.dict()
    order_dict["id"] = order_id
    order_dict["timestamp"] = datetime.now().isoformat()
    orders_db.append(order_dict)
    return {"order_id": order_id}


@app.get("/orders/")
async def list_orders(skip: int = 0, limit: int = 10):
    return orders_db[skip: skip + limit]


@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.patch("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    target_product = next((p for p in products_db if p["id"] == product_id), None)
    if not target_product:
        raise HTTPException(status_code=404, detail="Product not found")
    target_product["available_quantity"] = product.available_quantity
    return target_product
