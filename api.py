# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Модель для данных пользователя
class User(BaseModel):
    email: str
    full_name: str

# Словарь для временного хранения пользователей
user_data: Dict[str, User] = {}

# Маршрут для создания пользователя (POST)
@app.post("/user")
async def create_user(user: User) -> dict:
    if user.email in user_data:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_data[user.email] = user
    return {"message": f"User {user.full_name} added successfully"}

# Маршрут для получения информации о пользователе (GET)
@app.get("/user/{email}")
async def get_user(email: str) -> dict:
    user = user_data.get(email)
    if user:
        return user.dict()
    raise HTTPException(status_code=404, detail="User not found")
