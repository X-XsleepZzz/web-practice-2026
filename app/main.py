from fastapi import FastAPI

from app.api.routes import applications, companies

app = FastAPI()

@app.get("/")
def root():
    return {"message": "job tracker api"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

app.include_router(applications.router)
app.include_router(companies.router)
