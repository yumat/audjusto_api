from typing import List
from fastapi import APIRouter
import app.schemas.members as members_schema
from boto3.dynamodb.conditions import Key
import app.connect_db as connect_db

router = APIRouter()
members_table = connect_db.members_table

@router.get("/api/members/{group_id}", response_model=List[members_schema.Member])
async def read_members(group_id: str):
    res = members_table.query(
        KeyConditionExpression=Key('group_id').eq(group_id)
        )
    # print(res)
    response = res['Items']
    return response
