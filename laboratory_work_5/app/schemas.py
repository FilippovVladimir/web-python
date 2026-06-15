from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class LoginRequest(BaseModel):
    username: str
    password: str


class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(min_length=6, max_length=100)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class ProjectRead(ProjectCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int


class ProjectDetail(ProjectRead):
    tasks: list["TaskRead"] = Field(default_factory=list)


class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=700)
    deadline: datetime | None = None
    priority: int = Field(default=3, ge=1, le=5)
    status: str = Field(default="todo", max_length=30)
    project_id: int


class TaskUpdate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=700)
    deadline: datetime | None = None
    priority: int = Field(default=3, ge=1, le=5)
    status: str = Field(default="todo", max_length=30)
    project_id: int


class TaskRead(TaskCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


class TagCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)


class TagUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=50)


class TagRead(TagCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TaskTagCreate(BaseModel):
    tag_id: int
    relation_note: str | None = Field(default=None, max_length=200)


class TaskTagRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tag: TagRead
    relation_note: str | None
    assigned_at: datetime


class TimeEntryCreate(BaseModel):
    minutes: int = Field(gt=0, le=1440)
    comment: str | None = Field(default=None, max_length=300)


class TimeEntryUpdate(BaseModel):
    minutes: int = Field(gt=0, le=1440)
    comment: str | None = Field(default=None, max_length=300)


class TimeEntryRead(TimeEntryCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    created_at: datetime


class TaskDetail(TaskRead):
    tag_links: list[TaskTagRead] = Field(default_factory=list)
    time_entries: list[TimeEntryRead] = Field(default_factory=list)


ProjectDetail.model_rebuild()
