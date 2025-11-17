from typing import Any, Dict, Optional
from datetime import datetime
import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db

async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    db = await get_db()
    now = datetime.utcnow().isoformat()
    payload = {**data, "created_at": now, "updated_at": now}
    res = await db[collection_name].insert_one(payload)
    doc = await db[collection_name].find_one({"_id": res.inserted_id})
    if doc and "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc or payload

async def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 100):
    db = await get_db()
    cursor = db[collection_name].find(filter_dict or {}).limit(limit)
    items = []
    async for d in cursor:
        d["id"] = str(d.pop("_id"))
        items.append(d)
    return items
