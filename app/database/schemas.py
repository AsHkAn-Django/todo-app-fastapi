from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime



class TodoCreate(BaseModel):
    title: str
    description: Optional[str]
    completed: Optional[bool] = False
    created_at: Optional[datetime]


class TodoUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False


class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
