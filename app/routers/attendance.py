
from fastapi import APIRouter, HTTPException, status
import app.schemas.attendance as attendance_schema
from boto3.dynamodb.conditions import Key
import app.connect_db as connect_db
import shortuuid
import uuid

router = APIRouter()
possible_dates_table = connect_db.possible_dates_table
members_table = connect_db.members_table



@router.post("/api/attendance/{group_id}", response_model=attendance_schema.AttendanceCreateResponse)
async def create_pay(attendance_body: attendance_schema.AttendanceCreate, group_id: str):
    attendance = attendance_body.model_dump()
    member_uuid = create_member(group_id, attendance['name'])
    for date in attendance['dates']:
        add_vote(group_id, date['date_id'], member_uuid, attendance['name'], date['result'])
    return attendance


def create_member(group_uuid, name):
    u = uuid.uuid4()
    member_uuid = shortuuid.encode(u)
    member_data = {
        "name":name,
    }
    member_data['group_id'] = group_uuid
    member_data['member_id'] = member_uuid
    member_data['pay'] = 0
    member_data['paid'] = 0
    members_table.put_item(Item=member_data)
    return member_uuid


def add_vote(group_uuid, date_uuid, member_uuid, name, result):
    member_data = {
        "name":name,
        "member_id":member_uuid
    }
    possible_dates_res = possible_dates_table.get_item(
        Key={
            'group_id': group_uuid,
            'date_id': date_uuid
            }) 
    possible_dates_data = possible_dates_res['Item']
    possible_dates_data[result].append(member_data)
    print('a')
    possible_dates_table.put_item(Item=possible_dates_data)

