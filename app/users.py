from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

## uvicorn app.users:app --reload
##  http://127.0.0.1:8000 

@app.get("/")
async def root():
    return {"message": "API de usuarios funcionando"}


class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [
    User(id=1, name="gerardo", surname="Vazquez", age=44, url="https://gerardo.dev"),
    User(id=2, name="santiago", surname="Tovar", age=40, url="https://santiago.com"),
    User(id=3,name="jonathan", surname="Zurita", age=35, url="https://jonathan.dev")
]
        
        

@app.get("/usersjson")
async def usersjson():
    return [{"name": "Gerardo", "surname": "Vazquez","age":44, "url": "https://gerardo.dev"},
            {"name": "Santiago", "surname": "Tovar","age":40, "url": "https://santiago.com"},
            {"name": "Jonathan", "surname": "Zurita","age":35, "url": "https://jonathan.dev"}]
 
@app.get("/users")
async def users():
    return users_list


@app.get("/user/{id}")  # Path
async def user(id: int):
    return search_user(id)



# Endpoint alternativo para /userquery
@app.get("/userquery")
async def user_query_alt(id: int):
    return search_user(id)

@app.get("/user/")  # Query
async def user_query(id: int):
    return search_user(id)


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}