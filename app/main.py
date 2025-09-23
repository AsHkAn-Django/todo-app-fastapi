from fastapi import FastAPI
from app.database.session import Base, engine
from app.routers import todos


Base.metadata.create_all(bind=engine)
app = FastAPI(title="ToDo App")


app.include_router(todos.router)