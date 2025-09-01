from fastapi import FastAPI
from app.routers import products, users
from fastapi.staticfiles import StaticFiles
from app.routers import basic_auth_users

app = FastAPI()

# Incluyendo el router de productos
app.include_router(products.router)
# Incluyendo el router de usuarios
app.include_router(users.router)
# Incluyendo el router de autenticación básica
app.include_router(basic_auth_users.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
# uvicorn app.main:app --reload
##  http://127.0.0.1:8000 

## http://127.0.0.1:8000/static/images/python.jpg

@app.get("/")
async def root():
    return "Hola Fastapi"

@app.get("/url")
async def url():
    return { "url":"https://mouredev.com/python" }

