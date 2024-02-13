from typing import Annotated, List

from fastapi import (
    FastAPI,
    File,
    HTTPException,
    Body,
    Cookie,
    File,
    Form,
    Header,
    Path,
    Query,
    status,
    File,
    UploadFile,
    APIRouter,
    Depends,
    Request,
)


from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..dependencies.dependencies import get_token_header
from datetime import date, datetime

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

Base = declarative_base()


class RefuelingReport(BaseModel):
    date: str
    site_id: str
    site_name: str
    fuel_level_before: str
    fuel_level_after: str
    comment: str
    running_hours: str


class SupplyPickupReport(BaseModel):
    date: str
    pickup_location: str
    contractor_name: str
    vehicle_rego: str
    number_of_drum: int
    sites: str
    oil_qty: int
    coolant_qty: int
    comment: str


SQLALCHEMY_DATABASE_URL = (
    "mysql+mysqlconnector://gideonzozingao:password123@localhost/mno"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.get("/", tags=["reports"])
async def read_reports():
    return [{"report": "This is a report 1"}, {"report": "This is a report 2"}]


@router.post("/genset_refueling")
async def read_refuelingreport(
    report: RefuelingReport, files: List[UploadFile] = File(...)
):
    return {"report": report, "file_size": len(files)}


@router.post("/supply_pickup")
async def read_refuelingreport(
    report1: SupplyPickupReport, files: List[UploadFile] = File(...)
):
    return {"report": report1, "file_size": len(files)}
