from fastapi import FastAPI


app = FastAPI(title="Task API", version="1.0")

@app.get("/")
def root():
    return {"title": "Task API", "version": "1.0", "endpoints": ["/"]}


@app.get("/health")
def health():
    return {"status": "ok"}
