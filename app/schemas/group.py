from typing import Optional, List

from pydantic import BaseModel, Field


class GroupBase(BaseModel):
    group_name: Optional[str] = Field(None, example="テストの会")
  
class GroupCreate(GroupBase):
    members: List[dict] = Field(..., min_items=2, examples=[[
                {
                    "name": "太郎"
                },
                {
                    "name": "次郎"
                }
            ]])
    pass

class GroupCreateResponse(BaseModel):
    group_id: Optional[str]= Field(None, example="WtG5GaD9tPdAasoEFrGR85")

class Group(GroupBase):
    group_id: Optional[str]= Field(None, example="WtG5GaD9tPdAasoEFrGR85")

