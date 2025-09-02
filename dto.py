# ---------------------------
# Modelos DTO (Data Transfer Object) definidos con Pydantic.
# Validan y estructuran los datos de entrada y salida de la API.
# ---------------------------

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from bson import ObjectId
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler: GetCoreSchemaHandler):
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v

        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)

        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, _handler):
        return {"type": "string"}

class ReportBase(BaseModel):
    title: str = Field(..., example="Vertimiento en canal X")
    description: Optional[str] = Field(None, example="Aceite y residuos observados")
    location: str = Field(..., example="Suba, Bogotá")
    severity: Optional[int] = Field(
        1, ge=1, le=5, example=3, description="Nivel de severidad (1=muy bajo, 5=crítico)"
    )
    reporter_email: Optional[EmailStr] = Field(None, example="ciudadano@example.com")

class ReportCreate(ReportBase):
    pass

class ReportUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    severity: Optional[int] = Field(None, ge=1, le=5)
    reporter_email: Optional[EmailStr] = None

class ReportInDB(BaseModel):
    id: PyObjectId = Field(alias="_id")
    title: str
    description: Optional[str] = None
    severity: Optional[int] = None
    created_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}