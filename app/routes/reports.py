from fastapi import FastAPI, File, HTTPException, Body, Cookie, File, Form, Header, Path, Query, status, UploadFile, APIRouter,Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..dependencies.dependencies import get_token_header
router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

Base = declarative_base()
class RefuelingReport(BaseModel):
    date: str
    site_id:str
    site_name:str
    fuel_level_before:str
    fuel_level_after:str
    comment: str
    running_hours:str
    
SQLALCHEMY_DATABASE_URL = (
    "mysql+mysqlconnector://gideonzozingao:password123@localhost/mno"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@router.get("/", tags=["reports"])
async def read_reports():
    return [{"report": "This is a report 1"}, {"report": "This is a report 2"}]

@router.get("/genset_refueling", tags=["reports"])
async def read_refuelingreport():
    return [{"report": "This is a report 1"}, {"report": "This is a report 2"}]
