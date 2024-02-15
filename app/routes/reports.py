from typing import Annotated, List
from PIL import Image
import io
import os
import shutil
from fastapi import (
    File,
    Form,
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


class SiteOutageReport(BaseModel):
    date: str
    site_id: str
    site_name: str
    outage_datetime: str
    outage_cause: str
    rectification: str
    comments: str


class FileData(BaseModel):
    filename: str
    contents: bytes


SQLALCHEMY_DATABASE_URL = (
    "mysql+mysqlconnector://gideonzozingao:password123@localhost/mno"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
UPLOAD_DIRECTORY = "uploads"


@router.get("/", tags=["reports"])
async def read_reports():
    return [{"report": "This is a report 1"}, {"report": "This is a report 2"}]


@router.post("/genset_refueling")
async def gen_refueling(
    # file: Annotated[bytes, File(...)],
    # request: Request,
    date: Annotated[date, Form(...)],
    site_id: Annotated[str, Form(...)],
    site_name: Annotated[str, Form(...)],
    fuel_level_before: Annotated[float, Form(...)],
    fuel_level_after: Annotated[float, Form(...)],
    comment: Annotated[str, Form(...)],
    running_hours: Annotated[float, Form(...)],
    capturedImages: list[UploadFile] = File(...),
):
    # file_content = await file.read()
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    file_contents = []
    file_paths = []
    saved_files = []
    for file in capturedImages:
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        saved_files.append(file_path)

        file_contents.append(
            {
                "filename": file.filename,
                "content_type": file.content_type,
                "content": await file.read(),
            }
        )
    # request_body = await request.body()
    form_data = {
        "date": date,
        "site_id": site_id,
        "site_name": site_name,
        "fuel_level_before": fuel_level_before,
        "fuel_level_after": fuel_level_after,
        "comment": comment,
        "running_hours": running_hours,
    }
    # print(request_body.decode())
    return {
        # "file_content": file_contents,
        "form_data": form_data,
        # "request_body": request_body.decode(),
    }


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


@router.post("/site_outage_report")
async def site_outage_report(
    date: Annotated[date, Form(...)],
    site_id: Annotated[str, Form(...)],
    site_name: Annotated[str, Form(...)],
    outage_datetime: Annotated[str, Form(...)],
    outage_cause:Annotated[str, Form(...)],
    rectification: Annotated[str, Form(...)],
    comments:Annotated[str, Form(...)],
    images: List[UploadFile] = File(...),
):

    # print(capturedImages.dict())
    # Handle capturedImages as needed
    saved_files = []
    for image in images:
        file_path = os.path.join(UPLOAD_DIRECTORY, image.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())
        saved_files.append(file_path)

    return {
        "date": date,
        "site_id": site_id,
        "site_name": site_name,
        "outage_datetime": outage_datetime,
        "outage_cause": outage_cause,
        "rectification": rectification,
        "comments": comments,
    }
