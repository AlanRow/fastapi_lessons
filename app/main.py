from fastapi import FastAPI
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
    
    if target_user is not None:
        return target_user

@app.post("/users")
def create_user(user: UserModel):
    user_dict = {
        "id": user.id,
        "name": user.name
    }
    users.append(user_dict)
    
    return user_dict

# Практика 1: юзер по id
# Создайте в общем пространстве имен переменную users со списком пользователей
# каждый пользователь, это словарь с двумя ключами: id и name
# добавьте endpoint users/{id}, который вернет объект пользователя с
# соответствующим id

# Практика 2
# Напишите на выбор любой из методов : 
# Update (PUT) или Delete (DELETE)