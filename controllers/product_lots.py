import json
import logging

from fastapi import HTTPException
from datetime import datetime
from models.product_lots import ProductLots, ProductLotUpdate
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_one( id: int ) -> ProductLots:
    selectscript = """

    SELECT PL.id
     , P.id as product_id
     , P.name as product_name
     , PL.purchase_date
     , PL.purchase_price
     , PL.initial_quantity
     , PL.current_stock
     , PL.created_datetime
       FROM [agro].[product_lots] as PL
     INNER JOIN [agro].[products] as P ON PL.product_id = P.id
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




async def get_all() -> list[ProductLots]:
    selectscript = """
    SELECT PL.id
     , P.id as product_id
     , P.name as product_name
     , PL.purchase_date
     , PL.purchase_price
     , PL.initial_quantity
     , PL.current_stock
     , PL.created_datetime
       FROM [agro].[product_lots] as PL
     INNER JOIN [agro].[products] as P ON PL.product_id = P.id
    """

    result_dict=[]
    
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def delete_product_lot(id: int) -> str:

    deletescript= """
    DELETE FROM [agro].[product_lots]
    WHERE [id] = ?;
    """

    params = [id];
    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def update_lot(lot_id: int, productlot: ProductLotUpdate) -> ProductLots:
    update_data = productlot.model_dump(exclude_none=True)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
    
    set_clause = ", ".join([f"[{key}] = ?" for key in update_data.keys()])
    
    updatescript = f"""
    UPDATE [agro].[product_lots]
    SET {set_clause}
    WHERE [id] = ?;
    """

    params = list(update_data.values())
    params.append(lot_id)

    try:
        await execute_query_json(updatescript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    sqlfind: str = """
     SELECT PL.id
     , P.id as product_id
     , P.name as product_name
     , PL.purchase_date
     , PL.purchase_price
     , PL.initial_quantity
     , PL.current_stock
     , PL.created_datetime
       FROM [agro].[product_lots] as PL
     INNER JOIN [agro].[products] as P ON PL.product_id = P.id
     WHERE PL.id = ? ;

    """
    result_dict = []
    
    try:
        result = await execute_query_json(sqlfind, params=[lot_id])
        result_dict = json.loads(result)
        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def create_product_lot ( product_lot : ProductLots ) -> ProductLots:

    current_timestamp = datetime.now()

    sqlscript: str = """
        INSERT INTO [agro].[product_lots] ([product_id], [purchase_date], [purchase_price], [initial_quantity], [current_stock], [created_datetime])
        VALUES (?, ?, ?, ?, ?, ?);
    """

    params = [
        product_lot.product_id
        , product_lot.purchase_date
        , product_lot.purchase_price
        , product_lot.initial_quantity
        , product_lot.current_stock
        , current_timestamp
    ]
    
    insert_result = None

    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    sqlfind: str = """
     SELECT PL.id
     , P.id as product_id
     , P.name as product_name
     , PL.purchase_date
     , PL.purchase_price
     , PL.initial_quantity
     , PL.current_stock
     , PL.created_datetime
       FROM [agro].[product_lots] as PL
     INNER JOIN [agro].[products] as P ON PL.product_id = P.id
     WHERE PL.product_id = ? AND PL.created_datetime = ?

    """

    params = [product_lot.product_id, current_timestamp]
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
    

    