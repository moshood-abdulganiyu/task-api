from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel 
from fastapi.exceptions import RequestValidationError
import db

app = FastAPI(title="Task API", version="1.0")
db.init_db()


########################## HELPERS ##########################

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
    """Describe this API."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health():
    """Check if the API is running."""
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    """Return every task."""
    return db.get_all_tasks()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Return one task, or 404 if it does not exist."""
    task = db.get_task(task_id)
    if task is None:
        return error(404, f"Task {task_id} not found")
    return task


@app.post("/tasks", status_code=201)
def create_task(body: TaskCreate):
    """Create a task. Title is required."""
    title = body.title.strip()
    if title == "":
        return error(400, "title must not be empty")
    return db.create_task(title)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, body: TaskUpdate):
    """Update the title and/or done flag of a task."""
    task = db.get_task(task_id)
    if task is None:
        return error(404, f"Task {task_id} not found")
    if body.title is None and body.done is None:
        return error(400, "send at least one of: title, done")

    new_title = task["title"]
    new_done = task["done"]
    if body.title is not None:
        if body.title.strip() == "":
            return error(400, "title must not be empty")
        new_title = body.title.strip()
    if body.done is not None:
        new_done = body.done

    return db.update_task(task_id, new_title, new_done)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task."""
    if not db.delete_task(task_id):
        return error(404, f"Task {task_id} not found")
    return Response(status_code=204)



# @app.get("/stats")
# def stats():
#     """Return counts of total, done and open tasks."""
#     total = len(tasks)
#     done = sum(1 for t in tasks if t["done"])
#     return {"total": total, "done": done, "open": total - done}


# @app.post("/reset")
# def reset():
#     """Restore the 3 example tasks."""
#     global next_id
#     tasks.clear()
#     tasks.extend(seed_tasks())
#     next_id = 4
#     return {"status": "reset"}

