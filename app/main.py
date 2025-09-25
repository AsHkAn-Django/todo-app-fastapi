from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database.session import Base, engine
from app.routers import todos_router, auth_router
from app.core.config import settings

from datetime import datetime, timezone


Base.metadata.create_all(bind=engine)
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)


# CORS
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


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
app.include_router(auth_router.router)
