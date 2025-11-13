from typing import Union

from fastapi import FastAPI
from utils.database import execute_query_json
from dotenv import load_dotenv
import os
import json



load_dotenv()


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Students"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/students")
async def get_all_students():
    sqlscripts = """
    SELECT [id]
        ,[firstname]
        ,[lastname]
        ,[idperson]
        ,[email]
        ,[age]
    FROM [academics].[students]
"""
    result = await execute_query_json(sqlscripts)
    result_dict = json.loads(result)
    return result_dict
    