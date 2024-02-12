from fastapi import FastAPI, File, HTTPException, Body, Cookie, File, Form, Header, Path, Query, status, UploadFile, APIRouter,Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..dependencies.dependencies import get_token_header
router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    phone = Column(String)
    residental_address = Column(String)


    # vehicle_rego=Column(String)
class User(BaseModel):
    username: str
    password: str


class UserAuth(BaseModel):
    username: str
    password: str

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
@router.get("/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.post("/authenticate")
async def authenticate_user(user:UserAuth):
    return {"username": "fakecurrentuser"}

@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
