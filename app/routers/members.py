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
    response = res['Items']
    return response


@router.get("/api/member/{group_id}/{member_id}", response_model=members_schema.Member)
async def read_members(group_id: str, member_id: str):
    member_res = members_table.get_item(
        Key={
            'group_id': group_id,
            'member_id': member_id
            })
    response = member_res['Item']
    return response