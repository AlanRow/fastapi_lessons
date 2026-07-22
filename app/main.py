from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
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
        "name": "Alex"
    },
    {
        "id": "30",
        "name": "Tanja"
    },
    {
        "id": "40",
        "name": "Peter"
    },
    {
        "id": "50",
        "name": "Nikolay"
    },
]

def find_user_by_id(userlist, id):
    for user in userlist:
        if user["id"] == id:
            return user

# HTML Templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/user/{id}", response_class=HTMLResponse)
async def hello_world(request: Request, id):
    user = find_user_by_id(users, id)
    
    return templates.TemplateResponse(request, "index.html", {
        "request": request,
        "user": user,
        "message": f'User with ID <{id}> is not found'
    })
    
# API
@app.get("/api/users")
def filter_users(limit: int = 5, page: int = 1):
    first_index = limit * (page - 1)
    last_index = limit * page
    return users[first_index:last_index]

@app.get("/api/users/{id}")
def get_user_by_id(id):
    target_user = find_user_by_id(users, id)
    
    if target_user is None:
        raise HTTPException(status_code=404, detail="User is not found")

    return target_user

@app.post("/api/users", response_model=UserModel, status_code=201)
def create_user(user: UserModel):
    user_data = user.dict()
    
    for existing_user in users:
        if existing_user["id"] == user_data["id"]:
            raise HTTPException(status_code=400, detail="User elready exists")
    
    users.append(user_data)
    return user_data

# Практика 1: Роль пользователя
# Добавьте пользователям параметр role
# (admin, user, moderator)
# Имя админа должно выделяться жирным (font-weight: bold)
# Имя модератора - курсивом (font-style: italic)
# Имя обычого пользователя - никак

