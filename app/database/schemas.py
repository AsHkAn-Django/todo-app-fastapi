from pydantic import BaseModel, ConfigDict, constr, Field
from typing import List, Optional, Dict
from typing import Annotated



class TodoCreate(BaseModel):
    title: Annotated[
        str,
        Field(..., min_length=1, max_length=100, example="Read a book")
    ]
    description: str | None = Field(None, example="Read 20 pages of Dune")
    completed: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "title": "Wash the dishes",
                "description": "Wash all the dishes in the sink and else"
            }
        }


class TodoUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False


class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)


class PaginatedTodos(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[TodoResponse]

    model_config = {"from_attributes": True}  # Pydantic v2