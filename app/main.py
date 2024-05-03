import os
from typing import List, Dict, Union, Generator
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./test.db")
TABLE_NAME = os.getenv("SQLALCHEMY_TABLE_NAME", "todos")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Todo(Base):
    __tablename__ = TABLE_NAME
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

class TodoCreate(BaseModel):
    title: str
    description: str

class TodoRead(BaseModel):
    id: int
    title: str
    description: str

class TodoUpdate(BaseModel):
    title: str
    description: str

# Database connection
def get_database() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

# Default routes
@app.get("/", response_model=Dict[str, str])
def root() -> Dict[str, str]:
    return {"message": "Hello, World"}

# Todo routes, create a new todo, get all todos, get a todo by id, update a todo by id, delete a todo by id
@app.post("/todos/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: Session = Depends(get_database)) -> TodoRead:
    db_todo = Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Get all todos
@app.get("/todos/", response_model=List[TodoRead])
def get_todos(db: Session = Depends(get_database)) -> List[TodoRead]:
    todos = db.query(Todo).all()
    return todos

# Get all todos, via HTML formatted file
@app.get("/todos_list/")
def get_todos_list():
    return FileResponse("static/todos.html")

# Get a todo by id
@app.get("/todos/{todo_id}", response_model=TodoRead)
def read_todo(todo_id: int, db: Session = Depends(get_database)) -> TodoRead:
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return db_todo

# Update a todo by id
@app.put("/todos/{todo_id}", response_model=TodoRead)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_database)) -> TodoRead:
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db_todo.title = todo.title
    db_todo.description = todo.description
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Delete a todo by id
@app.delete("/todos/{todo_id}", response_model=TodoRead)
def delete_todo(todo_id: int, db: Session = Depends(get_database)) -> TodoRead:
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return db_todo
