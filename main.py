# main.py
from fastapi import FastAPI
from controller import router
import models
from database import engine

app = FastAPI()

# Include the router from the controller
app.include_router(router)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)
