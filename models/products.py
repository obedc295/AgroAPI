from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Product(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID autoincrementable del producto"
    )
    
    category_id: int = Field(
        ...,
        description="ID de la categoría a la que pertenece el producto",
        examples=[1, 2]
    )
    
    name: str = Field(
        ...,
        description="Nombre del producto",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9%\s\-\.,\(\)]+$",
        examples=["Urea 46%", "Decis 10 EC", "Round-up", "Fórmula 12-24-12"]
    )
    
    description: Optional[str] = Field(
        ...,
        description="Descripción del producto",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9\s\-\.,\(\)%/]+$",
        examples=["Fertilizante nitrogenado de alta concentración", "Insecticida de contacto"]
    )
    
    unit_of_measure: str = Field(
        ...,
        description="Unidad de medida del producto",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9\s\-\.,\(\)]+$",
        examples=["Saco (43 kg)", "1 Litro", "Galón", "Quintal (100 lb)"]
    )

class ProductUpdate(BaseModel):
        id: Optional[int] = Field(
            default=None,
            description="ID autoincrementable del producto"
        )
        
        category_id: int = Field(
            default=None,
            description="ID de la categoría a la que pertenece el producto",
            examples=[1, 2]
        )
        
        name: str = Field(
            default=None,
            description="Nombre del producto",
            pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9%\s\-\.,\(\)]+$",
            examples=["Urea 46%", "Decis 10 EC", "Round-up", "Fórmula 12-24-12"]
        )
        
        description: Optional[str] = Field(
            default=None,
            description="Descripción del producto",
            pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9\s\-\.,\(\)%/]+$",
            examples=["Fertilizante nitrogenado de alta concentración", "Insecticida de contacto"]
        )
        
        unit_of_measure: str = Field(
            default=None,
            description="Unidad de medida del producto",
            pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9\s\-\.,\(\)]+$",
            examples=["Saco (43 kg)", "1 Litro", "Galón", "Quintal (100 lb)"]
        )