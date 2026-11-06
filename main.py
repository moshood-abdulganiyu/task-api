from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel 
from fastapi.exceptions import RequestValidationError


app = FastAPI(title="Task API", version="1.0")

tasks = [
    {"id": 1, "title": "Learn what an API is", "done": True},
    {"id": 2, "title": "Build my first endpoint", "done": False},
    {"id": 3, "title": "Push my code to GitHub", "done": False},
]

next_id = 4

########################## HELPERS ##########################

def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def error(status_code: int, message: str):
    return JSONResponse(status_code=status_code, content={"error": message})


@app.exception_handler(RequestValidationError)
async def handle_validation_error(request: Request, exc: RequestValidationError):
    first = exc.errors()[0]
    where = ".".join(str(part) for part in first["loc"])
    return error(400, f"Invalid request - {where}: {first['msg']}")


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


########################## ENDPOINTS ##########################

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


@app.post("/tasks", status_code=201)
def create_task(body: TaskCreate):
    global next_id
    title = body.title.strip()
    if title == "":
        return error(400, "title must not be empty")
    new_task = {"id": next_id, "title": title, "done": False}
    next_id += 1
    tasks.append(new_task)
    return new_task



@app.put("/tasks/{task_id}")
def update_task(task_id: int, body: TaskUpdate):
    task = find_task(task_id)
    if task is None:
        return error(404, f"Task {task_id} not found")
    if body.title is None and body.done is None:
        return error(400, "send at least one of: title, done")
    if body.title is not None:
        if body.title.strip() == "":
            return error(400, "title must not be empty")
        task["title"] = body.title.strip()
    if body.done is not None:
        task["done"] = body.done
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        return error(404, f"Task {task_id} not found")
    tasks.remove(task)
    return Response(status_code=204)