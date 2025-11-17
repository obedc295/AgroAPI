import json
import logging

from fastapi import HTTPException

from models.categories import Category, CategoryUpdate
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_one( id: int ) -> Category:
    selectscript = """
            SELECT [id]
                ,[name]
                ,[description]
            FROM [agro].[categories]
                WHERE id = ?;
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




async def get_all() -> list[Category]:
    selectscript = """
    SELECT [id]
      ,[name]
      ,[description]
  FROM [agro].[categories]
    """

    result_dict=[]
    
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def delete_category(id: int) -> str:

    deletescript= """
    DELETE FROM [agro].[categories]
    WHERE [id] = ?;
    """

    params = [id];
    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")



async def update_category(category_id: int, category: CategoryUpdate) -> Category:
    update_data = category.model_dump(exclude_none=True)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
    
    set_clause = ", ".join([f"[{key}] = ?" for key in update_data.keys()])
    
    updatescript = f"""
    UPDATE [agro].[categories]
    SET {set_clause}
    WHERE [id] = ?;
    """

    params = list(update_data.values())
    params.append(category_id)

    try:
        await execute_query_json(updatescript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # Buscar por ID
    sqlfind = """
    SELECT [id], [name], [description]
    FROM [agro].[categories]
    WHERE id = ?;
    """

    params = [category_id]
    
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)
        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")




async def create_category ( category : Category ) -> Category:
    sqlscript: str = """
        INSERT INTO [agro].[categories] ([name], [description])
        VALUES (?, ?);
    """

    params = [
          category.name
        , category.description
    ]

    insert_result = None

    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    sqlfind: str = """
    SELECT [id]
      ,[name]
      ,[description]
    FROM [agro].[categories]
    WHERE name = ?;
    """

    params = [category.name]
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
    

    