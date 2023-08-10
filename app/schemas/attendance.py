from typing import Optional, List
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class ResultName(str, Enum):
    available = "available"
    maybe = "maybe"
    unavailable = "unavailable"


class AttendanceBase(BaseModel):
    name: Optional[str] = Field(None, example="太郎")

  
class DateBase(BaseModel):
    date: Optional[str] = Field(None, example="20230815")
    date_id: Optional[str] = Field(None, example="WtG5GaD9tPdAasoEFrGR85")
    result: Optional[ResultName] = Field(None, example="available")

class AttendanceCreate(AttendanceBase):
    dates: List[DateBase] = Field(None, examples=[[
                {
                    "date": "20230815",
                    "date_id": "WtG5GaD9tPdAasoEFrGR85",
                    "result": "available"
                },
                {
                    "date": "20230816",
                    "date_id": "WtG5GaD9tPdAasoEFrGR85",
                    "result": "maybe"
                }
            ]])
    pass


class AttendanceCreateResponse(AttendanceCreate):
    pass

class Attendance(AttendanceBase):
    dates: List[DateBase] = Field(None, examples=[[
                {
                    "date": "20230815",
                    "date_id": "WtG5GaD9tPdAasoEFrGR85",
                    "result": "available"
                },
                {
                    "date": "20230816",
                    "date_id": "WtG5GaD9tPdAasoEFrGR85",
                    "result": "maybe"
                }
            ]])
    pass

