from typing import Annotated, List
from PIL import Image
import io
from fastapi import (
    File,
    Request,
    UploadFile,
    APIRouter,
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
    responses={404: {"description": "Not found"}},
)

Base = declarative_base()


class RefuelingReport(BaseModel):
    date: str
    site_id: str
    site_name: str
    fuel_level_before: float
    fuel_level_after: float
    comment: str
    running_hours: int


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


class FileData(BaseModel):
    filename: str
    contents: bytes


SQLALCHEMY_DATABASE_URL = (
    "mysql+mysqlconnector://gideonzozingao:password123@localhost/mno"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.get("/", tags=["reports"])
async def read_reports():
    return [{"report": "This is a report 1"}, {"report": "This is a report 2"}]


@router.post("/genset_refueling")
async def gen_refueling(files: UploadFile = File(...)):
    return {"file": files.__dict__}


@router.post("/supply_pickup")
async def read_supply_pickup_report(
    report1: SupplyPickupReport, files: List[bytes] = File(...)
):
    # Access the submitted report data
    report_data = report1.dict()

    # Access individual fields of the report
    date = report_data["date"]
    pickup_location = report_data["pickup_location"]
    # etc.

    # Access the uploaded files
    file_names = [file.filename for file in files]
    file_sizes = [file.file._size for file in files]

    return {"report": report_data, "file_names": file_names, "file_sizes": file_sizes}
