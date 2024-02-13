from fastapi import FastAPI, File, HTTPException, Body, Cookie, File, Form, Header, Path, Query, status, UploadFile, APIRouter, Depends
from .routes import  users, reports
from .dependencies.dependencies import get_query_token, get_token_header

app = FastAPI()

app.include_router(users.router)
app.include_router(reports.router)

@app.get("/")
async def root():
    return {"message": "Hello from the server"}

