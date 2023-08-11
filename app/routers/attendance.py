
from fastapi import APIRouter, HTTPException, status
import app.schemas.attendance as attendance_schema
from boto3.dynamodb.conditions import Key
import app.connect_db as connect_db
import shortuuid
import uuid

router = APIRouter()
possible_dates_table = connect_db.possible_dates_table
members_table = connect_db.members_table


@router.get("/api/attendance/{group_id}/{member_id}", response_model=attendance_schema.Attendance)
async def read_schedule(group_id: str, member_id:str):
    
    response = {
        "name": None,
        "member_id": member_id,
        "dates": []
    }
    member_res = members_table.get_item(
        Key={
            'group_id': group_id,
            'member_id': member_id
        })
    response['name'] = member_res['Item']['name']
    res = possible_dates_table.query(
        KeyConditionExpression=Key('group_id').eq(group_id)
        )
    possible_dates = res['Items']
    for possible_date in possible_dates:
        result = 'available' if any(member['member_id'] == member_id for member in possible_date['available']) \
            else 'maybe' if any(member['member_id'] == member_id for member in possible_date['maybe']) \
            else 'unavailable' if any(member['member_id'] == member_id for member in possible_date['unavailable']) \
            else 'not_found'

        temp_data = {
            "date": possible_date['date'],
            "date_id": possible_date['date_id'],
            "result": result
        }
        response['dates'].append(temp_data)

    return response


@router.post("/api/attendance/{group_id}", response_model=attendance_schema.AttendanceCreateResponse)
async def create_pay(attendance_body: attendance_schema.AttendanceCreate, group_id: str):
    attendance = attendance_body.model_dump()
    if attendance['member_id'] == None:

        member_uuid = create_member(group_id, attendance['name'])
        for date in attendance['dates']:
            add_vote(group_id, date['date_id'], member_uuid, attendance['name'], date['result'])
        return attendance
    else:
        modify_member_name(group_id, attendance['member_id'], attendance['name'])
        for date in attendance['dates']:
            delete_vote(group_id, date['date_id'], attendance['member_id'])
            add_vote(group_id, date['date_id'], attendance['member_id'], attendance['name'], date['result'])
        return attendance


@router.delete("/api/attendance/{group_id}")
async def delete_attendance(delete_member_body: attendance_schema.AttendanceDelete, group_id: str):
    delete_member_id_dict = delete_member_body.model_dump()
    delete_member(group_id, delete_member_id_dict['member_id'])
    res = possible_dates_table.query(
        KeyConditionExpression=Key('group_id').eq(group_id)
        )
    possible_dates = res['Items']
    for possible_date in possible_dates:
        delete_vote(group_id, possible_date['date_id'], delete_member_id_dict['member_id'])



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


def modify_member_name(group_id, member_id, name):
    member_res = members_table.get_item(
        Key={
            'group_id': group_id,
            'member_id': member_id
            })
    member_data = member_res['Item']
    member_data['name'] = name
    members_table.put_item(Item=member_data)


def delete_member(group_id, member_id):
    member_res = members_table.get_item(
        Key={
            'group_id': group_id,
            'member_id': member_id
            })
    member_data = member_res['Item']
    if member_data['paid'] == 0 or member_data['pay'] == 0:
        members_table.delete_item(
        Key={
            'group_id': group_id,
            'member_id': member_id
            }
        )
    else:
        print('立替え記録が存在するため、メンバー削除を行いませんでした')
        

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
    possible_dates_table.put_item(Item=possible_dates_data)


def delete_vote(group_uuid, date_uuid, member_uuid):
    possible_dates_res = possible_dates_table.get_item(
        Key={
            'group_id': group_uuid,
            'date_id': date_uuid
            }) 
    possible_dates_data = possible_dates_res['Item']
    possible_dates_data['available'] = [member for member in possible_dates_data['available'] if member['member_id'] != member_uuid]
    possible_dates_data['maybe'] = [member for member in possible_dates_data['maybe'] if member['member_id'] != member_uuid]
    possible_dates_data['unavailable'] = [member for member in possible_dates_data['unavailable'] if member['member_id'] != member_uuid]
    possible_dates_table.put_item(Item=possible_dates_data)

