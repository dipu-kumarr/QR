from fastapi import FastAPI
from database import engine, Base
from routers import users

app = FastAPI()

# Include routers
app.include_router(users.router)

# Create database tables
Base.metadata.create_all(bind=engine)
