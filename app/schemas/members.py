from typing import Optional, List
from decimal import Decimal

from pydantic import BaseModel, Field



class MemberBase(BaseModel):
    name: Optional[str] = Field(None, example="太郎")

class Member(MemberBase):
    group_id: Optional[str] = Field(None, example="WtG5GaD9tPdAasoEFrGR85")
    member_id: Optional[str] = Field(None, example="WtG5GaD9tPdAasoEFrGR85")
    paid: Optional[Decimal] = Field(None, example=0)
    pay: Optional[Decimal] = Field(None, example=0)
    pass

