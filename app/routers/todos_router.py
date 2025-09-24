from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from sqlalchemy.orm import Session
from typing import List

from app.database import schemas
from app.database.session import get_db
from app.cruds import todos_crud


router = APIRouter(prefix="/todo", tags=["todos"])


@router.post(
    "/",
    summary="Create a new todo",
    description="This endpoint creates a new todo item with a title and"
    " optional description.",
    response_model=schemas.TodoResponse,
    status_code=201
)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return todos_crud.create_todo(db=db, todo=todo)


@router.get(
    "/",
    response_model=schemas.PaginatedTodos,
    summary="Get todo list",
    description="This endpoint brings the list of all the todos."
)
def list_todo(
    skip: int = 0,
    limit: int = 10,
    completed: bool | None = None,
    q: str | None = None,
    db: Session = Depends(get_db)
):
    total, todos = todos_crud.list_todo(
        db,
        skip=skip,
        limit=limit,
        completed=completed,
        q=q
    )
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": [schemas.TodoResponse.model_validate(todo) for todo in todos]
    }


@router.get(
    "/{todo_id}",
    response_model=schemas.TodoResponse,
    summary="Get todo item",
    description="This endpoint brings one single todo item."
)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = todos_crud.get_todo(db=db, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put(
    "/{todo_id}",
    response_model=schemas.TodoResponse,
    summary="Update a todo item",
    description="This endpoint updates one single todo item."
)
def update_todo(todo_id: int,
                todo_data: schemas.TodoUpdate,
                db: Session = Depends(get_db)):
    todo = todos_crud.update_todo(db=db, todo_id=todo_id, todo_data=todo_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.delete(
    "/{todo_id}",
    summary="Delete a todo item",
    description="This endpoint deletes a todo item."
)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    ok = todos_crud.delete_todo(db, todo_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
