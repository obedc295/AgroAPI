
from fastapi import HTTPException, APIRouter, status
from models.products import Product, ProductUpdate
from controllers.products import (
    create_product
    , update_product
    ,get_all
    ,get_one
    ,delete_product
)

router = APIRouter(prefix="/products")

@router.get("/", tags=["Products"], status_code=status.HTTP_200_OK)
async def get_all_products():
    result =  await get_all()
    return result

@router.get("/{id}", tags=["Products"], status_code=status.HTTP_200_OK)
async def get_one_product(id: int):
    result: Product = await get_one(id)
    return result


@router.post("/", tags=["Products"], status_code=status.HTTP_201_CREATED)
async def create_new_product(product_data: Product):
    result = await create_product(product_data)
    return result

@router.put("/{id}", tags=["Products"], status_code=status.HTTP_201_CREATED)
async def update_product_info(product_data: ProductUpdate, id: int):
    result = await update_product(id, product_data)
    return result

@router.delete("/{id}", tags=["Products"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_info(id: int):
   status: str =  await delete_product(id)
   return status





