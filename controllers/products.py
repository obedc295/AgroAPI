import json
import logging

from fastapi import HTTPException

from models.products import Product, ProductUpdate
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_one( id: int ) -> Product:
    selectscript = """

    SELECT P.id
        , P.name as product_name
        , P.category_id
        , C.name as category_name
        , P.description
        , P.unit_of_measure
      FROM [agro].[products] as P
      inner join [agro].[categories] as C on P.category_id = C.id
      WHERE P.id = ?;
            
    """
    result_dict = []
    try:
        result = await execute_query_json(selectscript, params=[id])
        result_dict = json.loads(result)
        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: {str(e)}")




async def get_all() -> list[Product]:
    selectscript = """
    SELECT P.id
        , P.name as product_name
        , P.category_id
        , C.name as category_name
        , P.description
        , P.unit_of_measure
      FROM [agro].[products] as P
      inner join [agro].[categories] as C on P.category_id = C.id
    """

    result_dict=[]
    
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def delete_product(id: int) -> str:

    deletescript= """
    DELETE FROM [agro].[products]
    WHERE [id] = ?;
    """

    params = [id];
    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def update_product(product_id: int, product: ProductUpdate) -> Product:
    update_data = product.model_dump(exclude_none=True)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
    
    set_clause = ", ".join([f"[{key}] = ?" for key in update_data.keys()])
    
    updatescript = f"""
    UPDATE [agro].[products]
    SET {set_clause}
    WHERE [id] = ?;
    """

    params = list(update_data.values())
    params.append(product_id)

    try:
        await execute_query_json(updatescript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    sqlfind: str = """
       SELECT P.id
        , P.name as product_name
        , P.category_id
        , C.name as category_name
        , P.description
        , P.unit_of_measure
      FROM [agro].[products] as P
      inner join [agro].[categories] as C on P.category_id = C.id
      WHERE P.id = ?;
    """

    result_dict=[]
    
    try:
        result = await execute_query_json(sqlfind, params=[product_id])
        result_dict = json.loads(result)
        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")



async def create_product ( product : Product ) -> Product:
    sqlscript: str = """
        INSERT INTO [agro].[products] ([category_id], [name], [description], [unit_of_measure])
        VALUES (?, ?, ?, ?);
    """

    params = [
        product.category_id
        , product.name
        , product.description
        , product.unit_of_measure
    ]
    
    insert_result = None

    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    sqlfind: str = """
       SELECT P.id
       , P.name as product_name
        , P.category_id
        , C.name as category_name
        , P.description
        , P.unit_of_measure
      FROM [agro].[products] as P
      inner join [agro].[categories] as C on P.category_id = C.id
      WHERE P.name = ? AND P.category_id = ?
    """

    params = [product.name, product.category_id]
    result_dict=[]
    
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)
        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

    