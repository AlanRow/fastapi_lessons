from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator

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
    age: int = 20
    name: str = Field(
        "Nobody",
        min_length=3,
        max_length=20,
        description="User's name"
    )
    surname: str = Field(
        "Nobody",
        min_length=3,
        max_length=20,
        description="User's name"
    )
    
    @field_validator("name")
    @classmethod
    def check_name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name must contain something")
        return v
    
    @model_validator(mode="after")
    def check_fullname_length(self):
        if len(self.name) + len(self.surname) > 50:
            raise ValueError("Full name must have 50 characters or lesser")
        return self
    

users = [
    {
        "id": "10",
        "name": "Gleb"
    },
    {
        "id": "20",
        "name": "Gleb"
    },
    {
        "id": "30",
        "name": "Gleb"
    },
    {
        "id": "40",
        "name": "Gleb"
    },
    {
        "id": "50",
        "name": "Gleb"
    },
    {
        "id": "60",
        "name": "Gleb"
    },
    {
        "id": "70",
        "name": "Gleb"
    },
    {
        "id": "80",
        "name": "Gleb"
    },
    {
        "id": "90",
        "name": "Gleb"
    }
]

def find_user_by_id(userlist, id):
    for user in userlist:
        if user["id"] == id:
            return user

@app.get("/users")
def filter_users(limit: int = 5, page: int = 1):
    first_index = limit * (page - 1)
    last_index = limit * page
    return users[first_index:last_index]

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

# Практика 1: Реализуйте фильтрацию пользователей
# по имени - должны вернуться по запросы только
# пользователи, чье имя содержит текст, отправленный
# в query-параметре search

# ПРИМЕЧАНИЕ: для поиска по тексту используйте 
# синтаксис Python: search in name

