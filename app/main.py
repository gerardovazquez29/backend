from fastapi import FastAPI
from app.routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Incluyendo el router de productos
app.include_router(products.router)
# Incluyendo el router de usuarios
app.include_router(users.router)
# Incluyendo el router de autenticación básica
app.include_router(basic_auth_users.router)
# Incluyendo el router de autenticación JWT
app.include_router(jwt_auth_users.router)
# Incluyendo el router de usuarios en la base de datos
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


# uvicorn app.main:app --reload

##  http://127.0.0.1:8000 

## http://127.0.0.1:8000/static/images/python.jpg

## antes de iniciar mongo en visualStudioCode , iniciar en terminal
## mongod

# Para ejecutar mongo db
## mongodb://localhost:27017

@app.get("/")
async def root():
    return "Hola Fastapi"

@app.get("/url")
async def url():
    return { "url":"https://mouredev.com/python" }

