from typing import Optional, List

from pydantic import BaseModel, Field


class ScheduleBase(BaseModel):
    group_name: Optional[str] = Field(None, example="テストの会")

class PossibleDatesBase(BaseModel):
    date: Optional[str] = Field(None, example="20230814")

class Member(BaseModel):
    name: Optional[str] = Field(None, example="太郎")
    member_id: Optional[str] = Field(None, example="WtG5GaD9tPdAasoEFrGR85")

class Schedule(PossibleDatesBase    ):
    date_id: Optional[str] = Field(None, example="AAG5GaD9tPdAasoEFrGR85")
    available:List[Member] = Field(None)
    maybe:List[Member] = Field(None)
    unavailable:List[Member] = Field(None)

class ScheduleCreate(ScheduleBase):
    schedule: List[PossibleDatesBase] = Field(..., min_items=2, examples=[[
                {
                    "date": "20230814"
                },
                {
                    "date": "20230815"
                }
            ]])
    pass


class ScheduleCreateResponse(BaseModel):
    group_id: Optional[str]= Field(None, example="WtG5GaD9tPdAasoEFrGR85")


