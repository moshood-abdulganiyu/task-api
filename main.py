from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI(title="Task API", version="1.0")

tasks = [
    {"id": 1, "title": "Learn what an API is", "done": True},
    {"id": 2, "title": "Build my first endpoint", "done": False},
    {"id": 3, "title": "Push my code to GitHub", "done": False},
]

next_id = 4

def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def error(status_code: int, message: str):
    return JSONResponse(status_code=status_code, content={"error": message})


@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        return error(404, f"Task {task_id} not found")
    return task


