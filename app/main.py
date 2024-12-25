# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURLを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/todo")
async def get_todos():
    return [{"id": 1, "title": "Sample Task", "completed": False},{"id": 1, "title": "Sample Task", "completed": False}]
