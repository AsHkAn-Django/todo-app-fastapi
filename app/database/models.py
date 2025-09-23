from sqlalchemy import (
    Column, Integer, String, ForeignKey, Text, DateTime, func, Boolean, JSON
)
from sqlalchemy.orm import relationship
from app.database.session import Base



class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
