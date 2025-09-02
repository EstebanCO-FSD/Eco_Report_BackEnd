# ---------------------------
# Clase DAO (Data Access Object) que encapsula la lógica de acceso a la base de datos MongoDB.
# ---------------------------

from typing import List, Optional
from bson import ObjectId

class ReportDAO:
    def __init__(self, db):
        self._col = db.get_collection("reports")

    async def create(self, report_data: dict) -> dict:
        result = await self._col.insert_one(report_data)
        return await self._col.find_one({"_id": result.inserted_id})

    async def get_by_id(self, id: str) -> Optional[dict]:
        if not ObjectId.is_valid(id):
            return None
        return await self._col.find_one({"_id": ObjectId(id)})

    async def list(self, skip: int = 0, limit: int = 50) -> List[dict]:
        cursor = self._col.find().skip(skip).limit(limit)
        return [doc async for doc in cursor]

    async def update(self, id: str, update_data: dict) -> Optional[dict]:
        if not ObjectId.is_valid(id):
            return None
        await self._col.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        return await self.get_by_id(id)

    async def delete(self, id: str) -> bool:
        if not ObjectId.is_valid(id):
            return False
        result = await self._col.delete_one({"_id": ObjectId(id)})
        return result.deleted_count == 1