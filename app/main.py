from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator

app = FastAPI()

# GET - получение данных, можно кэшировать -> Read - v
# POST - создание и (иногда) изменение -> Create
# PUT, PATCH - изменение данных -> Update
#   PUT - полное обновление
#   PATCH - частичное обновление данных
# DELETE - удаление данные -> Delete

# CRUD - Create-Read-Update-Delete

class UserModel(BaseModel):
    id: str
    name: str = Field(
        "Nobody",
        min_length=3,
        max_length=20,
        description="User's name"
    )
    
    @validator("name")
    def check_name_not_empty(self, v):
        if not v.strip():
            raise ValueError("Name must contain something")
        return v

users = [
    {
        "id": "10",
        "name": "Gleb"
    }
]

def find_user_by_id(userlist, id):
    for user in userlist:
        if user["id"] == id:
            return user

@app.get("/users/{id}")
def get_user_by_id(id):
    target_user = find_user_by_id(users, id)
    
    if target_user is None:
        raise HTTPException(status_code=404, detail="User is not found")

    return target_user

@app.post("/users", response_model=UserModel, status_code=201)
def create_user(user: UserModel):
    user_data = user.dict()
    
    for existing_user in users:
        if existing_user["id"] == user_data["id"]:
            raise HTTPException(status_code=400, detail="User elready exists")
    
    users.append(user_data)
    return user_data

# Практика 1: ошибка при создании
# Если при создании пользователя пользователь с таким id уже существует 
#  Вернуть ошибку 400 с комментарием "User already exists"

# Практика 2: пароль
# Добавьте поле password со следующими ограничениями:
# - не меньше 8 символов
# - не больше 30 символов
# - хотя бы один символ верхнего регистра, один - нижнего
#   и одна цифра