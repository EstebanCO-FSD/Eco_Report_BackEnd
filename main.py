# ---------------------------
# Archivo principal de la aplicación FastAPI.
# Se encarga de inicializar la app, definir rutas y conectar los servicios.
# ---------------------------

from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from typing import List
from datetime import datetime
from bson import ObjectId

from dao import ReportDAO
from dto import ReportCreate, ReportUpdate, ReportInDB
from db import db, client

report_dao = ReportDAO(db)

app = FastAPI(
    title="API Reportes de Fuentes de Contaminación - Bogotá",
    description="API para crear, listar, actualizar y eliminar reportes.",
    version="0.1.0"
)

def convert_objectid(doc: dict) -> dict:
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc

@app.post("/reports", response_model=ReportInDB, status_code=status.HTTP_201_CREATED)
async def create_report(report: ReportCreate):
    report_json = jsonable_encoder(report)
    report_json["created_at"] = datetime.utcnow()
    created = await report_dao.create(report_json)

    if not created:
        raise HTTPException(status_code=500, detail="Error creating report")
    
    return ReportInDB(**convert_objectid(created))

@app.get("/reports", response_model=List[ReportInDB])
async def list_reports(skip: int = 0, limit: int = 50):
    reports = await report_dao.list(skip=skip, limit=limit)
    return [ReportInDB(**convert_objectid(r)) for r in reports]

@app.get("/reports/{report_id}", response_model=ReportInDB)
async def get_report(report_id: str):
    doc = await report_dao.get_by_id(report_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Report not found")
    return ReportInDB(**convert_objectid(doc))

@app.put("/reports/{report_id}", response_model=ReportInDB)
async def update_report(report_id: str, report: ReportUpdate):
    update_data = jsonable_encoder(report, exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update fields provided")
    
    updated = await report_dao.update(report_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Report not found or invalid id")
    
    return ReportInDB(**convert_objectid(updated))

@app.delete("/reports/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(report_id: str):
    success = await report_dao.delete(report_id)
    if not success:
        raise HTTPException(status_code=404, detail="Report not found or invalid id")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/health")
async def health_check():
    try:
        await client.admin.command("ping")
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))