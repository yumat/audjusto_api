from typing import Optional, List
from decimal import Decimal

from pydantic import BaseModel, Field


class PaybackBase(BaseModel):
    sender: Optional[str] = Field(None, example="太郎")
    receiver: Optional[str] = Field(None, example="次郎")
    amount: Optional[Decimal] = Field(None, example=5000)


class Payback(PaybackBase):
    pass

