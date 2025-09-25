from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import List, Optional, Dict
from typing import Annotated


# ---------- Todo ----------
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


# ---------- User ----------
class UserCreate(BaseModel):
    username: Annotated[
        str,
        Field(..., min_length=3, max_length=100, example="Killer94")
    ]
    email: EmailStr
    password: Annotated[str, Field(min_length=6)]


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


# ---------- Token ----------
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None
