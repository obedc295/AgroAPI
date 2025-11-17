from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Category(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID autoincrementable de la categoría"
    )
    
    name: str = Field(
        ...,
        description="Nombre de la categoría",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9\s\-_]+$",
        examples=["Fertilizantes", "Insecticidas"]
    )
    
    description: str = Field(
        default=None,
        description="Descripción de la categoría",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9\s\-\.,]+$",
        examples=["Productos para nutrición vegetal", "Control de plagas e insectos"]
    )

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        description="Nombre de la categoría",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9\s\-_]+$",
        examples=["Fertilizantes", "Insecticidas"]
                                 )
    description: Optional[str] = Field(
        default=None, 
        description="Descripción de la categoría",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9\s\-\.,]+$",
        examples=["Productos para nutrición vegetal", "Control de plagas e insectos"])