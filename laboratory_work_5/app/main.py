from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.parse_routes import router as parse_router
from app.auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.database import get_db
from app.models import Project, Tag, Task, TaskTag, TimeEntry, User
from app.schemas import (
    LoginRequest,
    PasswordChange,
    ProjectCreate,
    ProjectDetail,
    ProjectRead,
    TagCreate,
    TagRead,
    TagUpdate,
    TaskCreate,
    TaskDetail,
    TaskRead,
    TaskTagCreate,
    TaskUpdate,
    TimeEntryCreate,
    TimeEntryRead,
    TimeEntryUpdate,
    Token,
    UserCreate,
    UserRead,
)


app = FastAPI(
    title="Time Manager API",
    description="Простое FastAPI приложение для управления задачами и временем.",
    version="1.0.0",
)

app.include_router(parse_router)

Db = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def get_project_for_user(db: Session, project_id: int, user_id: int) -> Project:
    project = db.scalar(
        select(Project).where(Project.id == project_id, Project.owner_id == user_id)
    )
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def get_task_for_user(db: Session, task_id: int, user_id: int) -> Task:
    task = db.scalar(select(Task).where(Task.id == task_id, Task.user_id == user_id))
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Time Manager API is running"}


@app.post("/auth/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Db) -> User:
    existing_user = db.scalar(
        select(User).where((User.username == data.username) | (User.email == data.email))
    )
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/auth/login", response_model=Token)
def login(data: LoginRequest, db: Db) -> Token:
    user = db.scalar(select(User).where(User.username == data.username))
    if user is None or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return Token(access_token=create_access_token({"sub": user.username}))


@app.get("/users/me", response_model=UserRead)
def read_me(current_user: CurrentUser) -> User:
    return current_user


@app.get("/users", response_model=list[UserRead])
def list_users(db: Db, current_user: CurrentUser) -> list[User]:
    return list(db.scalars(select(User).order_by(User.id)).all())


@app.post("/users/change-password")
def change_password(data: PasswordChange, db: Db, current_user: CurrentUser) -> dict:
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    current_user.hashed_password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password changed"}


@app.get("/projects", response_model=list[ProjectRead])
def list_projects(db: Db, current_user: CurrentUser) -> list[Project]:
    return list(
        db.scalars(
            select(Project)
            .where(Project.owner_id == current_user.id)
            .order_by(Project.id)
        ).all()
    )


@app.post("/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    data: ProjectCreate,
    db: Db,
    current_user: CurrentUser,
) -> Project:
    project = Project(**data.model_dump(), owner_id=current_user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@app.get("/projects/{project_id}", response_model=ProjectDetail)
def read_project(project_id: int, db: Db, current_user: CurrentUser) -> Project:
    project = db.scalar(
        select(Project)
        .where(Project.id == project_id, Project.owner_id == current_user.id)
        .options(selectinload(Project.tasks))
    )
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.put("/projects/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int,
    data: ProjectCreate,
    db: Db,
    current_user: CurrentUser,
) -> Project:
    project = get_project_for_user(db, project_id, current_user.id)
    project.name = data.name
    project.description = data.description
    db.commit()
    db.refresh(project)
    return project


@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Db, current_user: CurrentUser) -> None:
    project = get_project_for_user(db, project_id, current_user.id)
    db.delete(project)
    db.commit()


@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(db: Db, current_user: CurrentUser) -> list[Task]:
    return list(
        db.scalars(
            select(Task).where(Task.user_id == current_user.id).order_by(Task.id)
        ).all()
    )


@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, db: Db, current_user: CurrentUser) -> Task:
    get_project_for_user(db, data.project_id, current_user.id)
    task = Task(**data.model_dump(), user_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.get("/tasks/{task_id}", response_model=TaskDetail)
def read_task(task_id: int, db: Db, current_user: CurrentUser) -> Task:
    task = db.scalar(
        select(Task)
        .where(Task.id == task_id, Task.user_id == current_user.id)
        .options(
            selectinload(Task.tag_links).selectinload(TaskTag.tag),
            selectinload(Task.time_entries),
        )
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Db,
    current_user: CurrentUser,
) -> Task:
    task = get_task_for_user(db, task_id, current_user.id)
    get_project_for_user(db, data.project_id, current_user.id)
    for field, value in data.model_dump().items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Db, current_user: CurrentUser) -> None:
    task = get_task_for_user(db, task_id, current_user.id)
    db.delete(task)
    db.commit()


@app.get("/tags", response_model=list[TagRead])
def list_tags(db: Db, current_user: CurrentUser) -> list[Tag]:
    return list(db.scalars(select(Tag).order_by(Tag.name)).all())


@app.post("/tags", response_model=TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(data: TagCreate, db: Db, current_user: CurrentUser) -> Tag:
    existing_tag = db.scalar(select(Tag).where(Tag.name == data.name))
    if existing_tag is not None:
        raise HTTPException(status_code=400, detail="Tag already exists")
    tag = Tag(name=data.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@app.get("/tags/{tag_id}", response_model=TagRead)
def read_tag(tag_id: int, db: Db, current_user: CurrentUser) -> Tag:
    tag = db.get(Tag, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@app.put("/tags/{tag_id}", response_model=TagRead)
def update_tag(
    tag_id: int,
    data: TagUpdate,
    db: Db,
    current_user: CurrentUser,
) -> Tag:
    tag = db.get(Tag, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    existing_tag = db.scalar(
        select(Tag).where(Tag.name == data.name, Tag.id != tag_id)
    )
    if existing_tag is not None:
        raise HTTPException(status_code=400, detail="Tag already exists")
    tag.name = data.name
    db.commit()
    db.refresh(tag)
    return tag


@app.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Db, current_user: CurrentUser) -> None:
    tag = db.get(Tag, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(tag)
    db.commit()


@app.post("/tasks/{task_id}/tags", status_code=status.HTTP_201_CREATED)
def add_tag_to_task(
    task_id: int,
    data: TaskTagCreate,
    db: Db,
    current_user: CurrentUser,
) -> dict[str, str]:
    get_task_for_user(db, task_id, current_user.id)
    tag = db.get(Tag, data.tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    link = TaskTag(
        task_id=task_id,
        tag_id=data.tag_id,
        relation_note=data.relation_note,
    )
    db.merge(link)
    db.commit()
    return {"message": "Tag added to task"}


@app.delete("/tasks/{task_id}/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_tag_from_task(
    task_id: int,
    tag_id: int,
    db: Db,
    current_user: CurrentUser,
) -> None:
    get_task_for_user(db, task_id, current_user.id)
    link = db.get(TaskTag, {"task_id": task_id, "tag_id": tag_id})
    if link is None:
        raise HTTPException(status_code=404, detail="Task tag not found")
    db.delete(link)
    db.commit()


@app.post(
    "/tasks/{task_id}/time-entries",
    response_model=TimeEntryRead,
    status_code=status.HTTP_201_CREATED,
)
def add_time_entry(
    task_id: int,
    data: TimeEntryCreate,
    db: Db,
    current_user: CurrentUser,
) -> TimeEntry:
    get_task_for_user(db, task_id, current_user.id)
    entry = TimeEntry(**data.model_dump(), task_id=task_id)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@app.get("/tasks/{task_id}/time-entries", response_model=list[TimeEntryRead])
def list_time_entries(
    task_id: int,
    db: Db,
    current_user: CurrentUser,
) -> list[TimeEntry]:
    get_task_for_user(db, task_id, current_user.id)
    return list(
        db.scalars(
            select(TimeEntry)
            .where(TimeEntry.task_id == task_id)
            .order_by(TimeEntry.created_at)
        ).all()
    )


@app.delete("/time-entries/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_time_entry(entry_id: int, db: Db, current_user: CurrentUser) -> None:
    entry = db.scalar(
        select(TimeEntry)
        .join(Task)
        .where(TimeEntry.id == entry_id, Task.user_id == current_user.id)
    )
    if entry is None:
        raise HTTPException(status_code=404, detail="Time entry not found")
    db.delete(entry)
    db.commit()


@app.put("/time-entries/{entry_id}", response_model=TimeEntryRead)
def update_time_entry(
    entry_id: int,
    data: TimeEntryUpdate,
    db: Db,
    current_user: CurrentUser,
) -> TimeEntry:
    entry = db.scalar(
        select(TimeEntry)
        .join(Task)
        .where(TimeEntry.id == entry_id, Task.user_id == current_user.id)
    )
    if entry is None:
        raise HTTPException(status_code=404, detail="Time entry not found")
    entry.minutes = data.minutes
    entry.comment = data.comment
    db.commit()
    db.refresh(entry)
    return entry
