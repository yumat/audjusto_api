from typing import List
from fastapi import APIRouter, HTTPException, status
import app.schemas.group as group_schema
import shortuuid
import uuid
from boto3.dynamodb.conditions import Key
import app.connect_db as connect_db

router = APIRouter()
group_table = connect_db.group_table
members_table = connect_db.members_table

@router.get("/api/group/{group_id}", response_model=group_schema.Group)
async def read_group(group_id: str):
    res = group_table.get_item(Key={"group_id": group_id})

    if 'Item' in res:
        response = {
            "group_name": res['Item']['group_name'],
            "group_id": res['Item']['group_id']
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{group_id} not found"
        )      
    return response


@router.post("/api/group", response_model=group_schema.GroupCreateResponse)
async def create_group(group_body: group_schema.GroupCreate):
    group = group_body.model_dump()
    u = uuid.uuid4()
    s_uuid = shortuuid.encode(u)

    group['group_id'] = s_uuid
    members = group.pop('members')
    group_table.put_item(Item=group)
    for member in members:
        u = uuid.uuid4()
        member_uuid = shortuuid.encode(u)        
        member['group_id'] = s_uuid
        member['member_id'] = member_uuid
        member['pay'] = 0
        member['paid'] = 0
        members_table.put_item(Item=member)
    response = {'group_id': s_uuid}
    return response


@router.post("/api/groupname", response_model=group_schema.Group)
async def modify_group(group_body: group_schema.Group):
    group = group_body.model_dump()
    group_table.put_item(Item=group)
    return group