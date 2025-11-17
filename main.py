from fastapi import FastAPI
from routes.products import router as router_product
from routes.categories import router as router_category
from routes.product_lots import router as router_product_lot

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Farmer!"}

app.include_router(router_product)
app.include_router(router_category)
app.include_router(router_product_lot)