from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Todo, User
from app.schemas import TodoCreate, TodoResponse
from app.database import get_db
from app.routes.auth import get_current_user
from typing import List

router = APIRouter(prefix="/todos", tags=["todos"])

# タスク一覧取得
@router.get("/", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Todo).filter(Todo.user_id == current_user.id).all()

# タスク作成
@router.post("/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_todo = Todo(**todo.dict(), user_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# タスク更新
@router.put("/{task_id}", response_model=TodoResponse)
def update_todo(task_id: int, todo: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_todo = db.query(Todo).filter(Todo.id == task_id, Todo.user_id == current_user.id).first()
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo.dict(exclude_unset=True).items():
        setattr(existing_todo, key, value)
    db.commit()
    db.refresh(existing_todo)
    return existing_todo

# タスク削除
@router.delete("/{task_id}")
def delete_todo(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == task_id, Todo.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "タスクが削除されました"}

# タスク完了/未完了の切り替え
@router.put("/{task_id}/toggle", response_model=TodoResponse)
def toggle_task_complete(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Todo).filter(Todo.id == task_id, Todo.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Todo not found")
    task.completed = not task.completed
    db.commit()
    db.refresh(task)
    return task
