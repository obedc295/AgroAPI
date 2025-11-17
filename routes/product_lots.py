from fastapi import HTTPException, APIRouter, status
from models.product_lots import ProductLots, ProductLotUpdate
from controllers.product_lots import (
    create_product_lot
    , update_lot
    , delete_product_lot
    , get_all
    , get_one
)

router = APIRouter(prefix="/product_lots")

@router.get("/", tags=["Product_lots"], status_code=status.HTTP_200_OK)
async def get_all_product_lots():
    result =  await get_all()
    return result

@router.get("/{id}", tags=["Product_lots"], status_code=status.HTTP_200_OK)
async def get_one_product_lot(id: int):
    result: ProductLots = await get_one(id)
    return result


@router.post("/", tags=["Product_lots"], status_code=status.HTTP_201_CREATED)
async def create_new_product_lot(product_lot_data: ProductLots):
    result = await create_product_lot(product_lot_data)
    return  result

@router.put("/{id}", tags=["Product_lots"], status_code=status.HTTP_201_CREATED)
async def update_lot_info(produc_lot_data: ProductLotUpdate, id: int):
    result = await update_lot(id, produc_lot_data)
    return result

@router.delete("/{id}", tags=["Product_lots"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_lot_info(id: int):
   status: str =  await delete_product_lot(id)
   return status