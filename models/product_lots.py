from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date
import re

class ProductLots(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID autoincrementable del lote"
    )
    
    product_id: int = Field(
        ...,
        description="ID del producto al que pertenece el lote",
        examples=[1, 2]
    )
    
    product_name: Optional[str] = Field(
        default=None,
        description="Nombre del producto (solo lectura)",
        examples=["Urea 46%", "Decis 10 EC"]
    )
    
    purchase_date: date = Field(
        ...,
        description="Fecha de compra del lote",
        examples=["2024-01-20"]
    )
    
    purchase_price: float = Field(
        ...,
        description="Precio de compra del lote",
        gt=0,
        examples=[650.00, 1200.00]
    )
    
    initial_quantity: float = Field(
        ...,
        description="Cantidad inicial del lote",
        gt=0,
        examples=[100, 50]
    )
    
    current_stock: float = Field(
        ...,
        description="Stock actual del lote",
        ge=0,
        examples=[100, 45]
    )
    
    @field_validator('purchase_date')
    @classmethod
    def validate_purchase_date(cls, v):
        if v > date.today():
            raise ValueError('La fecha de compra no puede ser futura')
        return v


class ProductLotUpdate(BaseModel):
    product_id: Optional[int] = Field(
        default=None,
        description="ID del producto al que pertenece el lote",
        examples=[1, 2, 3]
    )
    
    purchase_date: Optional[date] = Field(
        default=None,
        description="Fecha de compra del lote",
        examples=["2024-01-20", "2024-02-15"]
    )
    
    purchase_price: Optional[float] = Field(
        default=None,
        description="Precio de compra del lote",
        gt=0,
        examples=[650.00, 1200.00, 850.50]
    )
    
    initial_quantity: Optional[float] = Field(
        default=None,
        description="Cantidad inicial del lote",
        gt=0,
        examples=[100.00, 50.00, 200.00]
    )
    
    current_stock: Optional[float] = Field(
        default=None,
        description="Stock actual del lote",
        ge=0,
        examples=[100.00, 45.00, 150.00]
    )
    
    @field_validator('purchase_date')
    @classmethod
    def validate_purchase_date(cls, v):
        if v and v > date.today():
            raise ValueError('La fecha de compra no puede ser futura')
        return v