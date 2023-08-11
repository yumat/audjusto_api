from typing import List
from fastapi import APIRouter, HTTPException, status
import app.schemas.schedule as schedule_schema
import shortuuid
import uuid
from boto3.dynamodb.conditions import Key
import app.connect_db as connect_db

router = APIRouter()
group_table = connect_db.group_table
possible_dates_table = connect_db.possible_dates_table

@router.get("/api/schedule/{group_id}", response_model=List[schedule_schema.Schedule])
async def read_schedule(group_id: str):
    res = possible_dates_table.query(
        KeyConditionExpression=Key('group_id').eq(group_id)
        )
    # print(res)
    response = res['Items']
    response.sort(key=date_key)
    return response


def date_key(item):
    return item['date']


@router.post("/api/schedule", response_model=schedule_schema.ScheduleCreateResponse)
async def create_schedule(group_body: schedule_schema.ScheduleCreate):
    group = group_body.model_dump()
    u = uuid.uuid4()
    s_uuid = shortuuid.encode(u)

    group['group_id'] = s_uuid
    schedule = group.pop('schedule')
    group_table.put_item(Item=group)

    unique_dates = set()
    temp_schedule = []
    for item in schedule:
        date = item["date"]
        if date not in unique_dates:
            unique_dates.add(date)
            temp_schedule.append(item)

    for date in temp_schedule:
        u = uuid.uuid4()
        date_uuid = shortuuid.encode(u)        
        date['group_id'] = s_uuid
        date['date_id'] = date_uuid
        date['available'] = []
        date['maybe'] = []
        date['unavailable'] = []
        possible_dates_table.put_item(Item=date)
    response = {'group_id': s_uuid}
    return response
