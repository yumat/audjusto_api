from typing import Optional, List
from decimal import Decimal

from pydantic import BaseModel, Field


class PayBase(BaseModel):
    payer: Optional[str] = Field(None, example="太郎")
    payer_id: Optional[str] = Field(None, example="WtG5GaD9tPdAasoEFrGR85")
    event: Optional[str] = Field(None, example="飲み会")
    amount: Optional[Decimal] = Field(None, example=5000)
  
class memberBase(BaseModel):
    name: Optional[str] = Field(None, example="太郎")
    member_id: Optional[str] = Field(None, example="WtG5GaD9tPdAasoEFrGR85")

class PayCreate(PayBase):
    members: List[memberBase] = Field(None, examples=[[
                {
                    "name": "太郎",
                    "member_id": "WtG5GaD9tPdAasoEFrGR85"
                },
                {
                    "name": "次郎",
                    "member_id": "WtG5GaD9tPdAasoEFrGR85"
                }
            ]])
    pass

class PayDelete(BaseModel):
    date_time: Optional[str] = Field(None, example="2023/08/07 22:35")
    pass

class PayCreateResponse(PayCreate):
    date_time: Optional[str] = Field(None, example="2023/08/07 22:35")
    pass

class Pay(PayBase):
    date_time: Optional[str] = Field(None, example="2023/08/07 22:35")
    members: List[memberBase] = Field(None, examples=[[
                {
                    "name": "太郎",
                    "member_id": "WtG5GaD9tPdAasoEFrGR85"
                },
                {
                    "name": "次郎",
                    "member_id": "WtG5GaD9tPdAasoEFrGR85"
                }
            ]])
    pass

