from typing import List
from fastapi import APIRouter, HTTPException, status
import app.schemas.pay as pay_schema
import datetime
from boto3.dynamodb.conditions import Key
import app.connect_db as connect_db
from decimal import Decimal

router = APIRouter()
pay_table = connect_db.pay_table
members_table = connect_db.members_table

@router.get("/api/pays/{group_id}", response_model=List[pay_schema.Pay])
async def read_pay(group_id: str):
    res = pay_table.query(
        KeyConditionExpression=Key('group_id').eq(group_id)
        )
    
    response = res['Items']
    return response


@router.post("/api/pay/{group_id}", response_model=pay_schema.PayCreateResponse)
async def create_pay(pay_body: pay_schema.PayCreate, group_id: str):
    pay = pay_body.model_dump()
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    d = now.strftime('%Y/%m/%d %H:%M:%S')
    pay['date_time'] = str(d)
    pay['group_id'] = group_id
    pay_table.put_item(Item=pay)
    # 支払者金額の処理
    payer_res = get_member_date(group_id, pay['payer_id'])
    culc_pay_amount(payer_res, pay['amount'])


    paid_amount = pay['amount'] / len(pay['members'])
    for member in pay['members']:
        paid_res = get_member_date(group_id, member['member_id'])
        culc_paid_amount(paid_res, paid_amount)
    return pay


@router.delete("/api/pay/{group_id}")
async def delete_pay(date_time_body: pay_schema.PayDelete, group_id: str):
    pay_date_time = date_time_body.model_dump()
    pay_res = pay_table.get_item(
        Key={
            'group_id': group_id,
            'date_time': pay_date_time['date_time']
            })    
    pay_res_data = pay_res['Item']
    delete_pay_data(group_id, pay_date_time['date_time'])
    print('payer modosi')
    payer_res = get_member_date(group_id, pay_res_data['payer_id'])
    culc_pay_amount(payer_res, -pay_res_data['amount'])
    print(' paid modosi')
    paid_amount = pay_res_data['amount'] / len(pay_res_data['members'])
    for member in pay_res_data['members']:
        paid_res = get_member_date(group_id, member['member_id'])
        culc_paid_amount(paid_res, -paid_amount)


    return pay_res_data


def culc_pay_amount(payer_data, amount):
    print()
    # payer_data = payer_res['Item']
    payer_data['pay'] = payer_data['pay'] + amount
    members_table.put_item(Item=payer_data)   


def culc_paid_amount(paid_data, paid_amount):
    print()
    # paid_data = paid_res['Item']
    paid_data['paid'] = paid_data['paid'] + Decimal(paid_amount)
    members_table.put_item(Item=paid_data)


def delete_pay_data(group_id, date_time):
    pay_table.delete_item(
        Key={
            'group_id': group_id,
            'date_time': date_time
            }
    )

def get_member_date(group_id, member_id):
    paid_res = members_table.get_item(
        Key={
            'group_id': group_id,
            'member_id': member_id
            })
    member_data = paid_res['Item']
    
    return member_data
