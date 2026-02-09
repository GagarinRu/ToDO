from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    telegram_id: Optional[int] = None
    telegram_username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    username: str
    password: str
    email: Optional[str] = None
    last_name: Optional[str] = None


class UserResponse(UserBase):
    id: str
    username: str
    email: Optional[str] = None
    is_active: bool
    date_joined: datetime

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str
    color: str = "#3498db"


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: str
    user: str
    created_at: datetime

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"
    priority: str = "medium"
    due_date: Optional[datetime] = None
    category_ids: Optional[List[str]] = Field(default_factory=list)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    category_ids: Optional[List[str]] = None


class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    user: str
    categories: List[CategoryResponse]

    class Config:
        from_attributes = True
