from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.database.session import Base, engine
from app.routers import todos_router

from datetime import datetime, timezone


Base.metadata.create_all(bind=engine)
app = FastAPI(title="ToDo App")


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": 500,
            "message": str(exc)
        }
    )


app.include_router(todos_router.router)
