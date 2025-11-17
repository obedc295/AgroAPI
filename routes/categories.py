
from fastapi import HTTPException, APIRouter, status
from models.categories import Category, CategoryUpdate
from controllers.categories import (
    create_category
    , update_category
    , delete_category
    , get_all
    , get_one
)

router = APIRouter(prefix="/categories")

@router.get("/", tags=["Categories"], status_code=status.HTTP_200_OK)
async def get_all_categories():
    result =  await get_all()
    return result

@router.get("/{id}", tags=["Categories"], status_code=status.HTTP_200_OK)
async def get_one_category(id: int):
    result: Category = await get_one(id)
    return result


@router.post("/", tags=["Categories"], status_code=status.HTTP_201_CREATED)
async def create_new_category(category_data: Category):
    result = await create_category(category_data)
    return result

@router.put("/{id}", tags=["Categories"], status_code=status.HTTP_201_CREATED)
async def update_category_info(category_data: CategoryUpdate, id: int):
    result = await update_category(id, category_data)
    return result

@router.delete("/{id}", tags=["Categories"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_info(id: int):
   status: str =  await delete_category(id)
   return status





