from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
    name: str

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
    user_dict = {
        "id": user.id,
        "name": user.name
    }
    users.append(user_dict)
    
    return user_dict

# Практика 1: ошибка при создании
# Если при создании пользователя пользователь с таким id уже существует 
#  Вернуть ошибку 400 с комментарием "User already exists"