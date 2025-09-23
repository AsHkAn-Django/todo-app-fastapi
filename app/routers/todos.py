from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List
from app.database import schemas
from app.database import models
from app.database.session import get_db


router = APIRouter(prefix="/todo", tags=["todos"])


@router.post("/", response_model=schemas.TodoCreate)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    td = models.Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
    )
    db.add(td)
    db.commit()
    db.refresh(td)
    return td


@router.get("/", response_model=List[schemas.TodoResponse])
def list_todo(db: Session = Depends(get_db)):
    todos = db.execute(select(models.Todo)).scalars().all()
    return todos


@router.get("/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
