from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from schemas import Application, ApplicationOut
from database import create_document, get_documents

app = FastAPI(title="Strategy Session Applications")

# Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

COLLECTION = "application"

@app.get("/", tags=["health"]) 
async def root():
    return {"status": "ok"}

@app.post("/apply", response_model=ApplicationOut, tags=["applications"]) 
async def apply(payload: Application):
    try:
        doc = await create_document(COLLECTION, payload.model_dump())
        return ApplicationOut(**doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/applications", response_model=List[ApplicationOut], tags=["applications"]) 
async def list_applications(limit: int = 50):
    try:
        docs = await get_documents(COLLECTION, {}, limit)
        return [ApplicationOut(**d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
