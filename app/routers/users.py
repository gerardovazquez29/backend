from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter()

## uvicorn app.users:app --reload
##  http://127.0.0.1:8000 

##  {"id": 4, "name":"jonathan", "surname":"Zurita", "age":35, "url":"https://jonathan.dev"}

@router.get("/")
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
        
        

@router.get("/usersjson")
async def usersjson():
    return [{"name": "Gerardo", "surname": "Vazquez","age":44, "url": "https://gerardo.dev"},
            {"name": "Santiago", "surname": "Tovar","age":40, "url": "https://santiago.com"},
            {"name": "Jonathan", "surname": "Zurita","age":35, "url": "https://jonathan.dev"}]

@router.get("/users")
async def users():
    return users_list


@router.get("/user/{id}")  # Path
async def user(id: int):
    return search_user(id)



# Endpoint alternativo para /userquery
@router.get("/userquery")
async def user_query_alt(id: int):
    return search_user(id)

@router.get("/user/")  # Query
async def user_query(id: int):
    return search_user(id)



@router.post("/user/", response_model=User, status_code=201)
async def user_post(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    users_list.append(user)
    return user

@router.put("/user/")
async def user_put(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "No se ha actualizado el usuario"}

    return user


@router.delete("/user/{id}")
async def user_delete(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error": "No se ha eliminado el usuario"}


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
    finally:
        pass
