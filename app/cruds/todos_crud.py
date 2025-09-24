from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import models, schemas


def create_todo(db: Session, todo: schemas.TodoCreate):
    td = models.Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
    )
    db.add(td)
    db.commit()
    db.refresh(td)
    return td


def list_todo(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    completed: bool | None = None,
    q: str | None = None
):
    query = db.query(models.Todo)

    if completed is not None:
        query = query.filter(models.Todo.completed == completed)

    if q:
        query = query.filter(
            (models.Todo.title.ilike(f"%{q}%")) |
            (models.Todo.description.ilike(f"%{q}%"))
        )

    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return total, items


def get_todo(db: Session, todo_id: int):
    return db.get(models.Todo, todo_id)


def update_todo(db: Session, todo_id: int, todo_data: schemas.TodoUpdate):
    todo = db.get(models.Todo, todo_id)
    if not todo:
        return None

    for key, value in todo_data.model_dump(exclude_unset=True).items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int):
    todo = db.get(models.Todo, todo_id)
    if not todo:
        return None

    db.delete(todo)
    db.commit()
    return True
