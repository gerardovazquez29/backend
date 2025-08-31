from fastapi import APIRouter


## uvicorn app.main:app --reload
##  http://127.0.0.1:8000 

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={
        404: {"message": "No encontrado"},
        200: {"message": "Éxito"}
    }
)

@router.get("/")
async def root():
    return {"message": "API de productos funcionando"}

products_list = ["Producto 1","Producto 2", "Producto 3", "Producto 4", "Producto 5"]

@router.get("/")
async def products():
    return products_list


@router.get("/{id}")
async def product(id: int):
    return products_list[id]


