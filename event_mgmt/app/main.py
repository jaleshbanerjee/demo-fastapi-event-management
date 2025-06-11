from fastapi import FastAPI
from api import routes
from db.database import engine, Base
import uvicorn
import asyncio
from fastapi.responses import HTMLResponse

from sqlalchemy.ext.asyncio import create_async_engine
from db.models import Base  
from db.database import engine 

app = FastAPI(title="Mini Event Management System")

# Include API routes
app.include_router(routes.router)

# Create tables on startup if you skip alembic migrations 
@app.on_event("startup")
async def on_startup():
    await init_models()

# Optional: Add a simple root endpoint
# @app.get("/")
@app.get("/" ,response_class=HTMLResponse, tags=["Home"])
async def home():
    return """
    <h1>Welcome to the Mini Event Management System API</h1>
    <p>HEAD OVER TO <a href="http://127.0.0.1:9000/docs">Click Here</a></p>
    """
 

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

