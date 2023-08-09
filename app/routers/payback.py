from typing import List
from fastapi import APIRouter, HTTPException, status
import app.schemas.payback as payback_schema
import datetime
from boto3.dynamodb.conditions import Key
import app.connect_db as connect_db
from decimal import Decimal

router = APIRouter()
# pay_table = connect_db.pay_table
members_table = connect_db.members_table

@router.get("/api/paybacks/{group_id}", response_model=List[payback_schema.Payback])
async def read_pay(group_id: str):
    res = members_table.query(
        KeyConditionExpression=Key('group_id').eq(group_id)
        )
    
    members = res['Items']
    for member in members:
        difference = member['pay'] - member['paid']
        member['difference'] = difference

    # 負の差分を持つメンバーと正の差分を持つメンバーに分ける
    debit_members = [member for member in members if member['difference'] < 0]
    credit_members = [member for member in members if member['difference'] > 0]

    # 支払い情報のリストを作成
    payments = []

    # 割り勘の計算と支払い情報の収集
    for debit_member in debit_members:
        for credit_member in credit_members:
            if abs(debit_member['difference']) < 1e-10:
            # if debit_member['difference'] == 0:
                break
            payment = min(abs(debit_member['difference']), credit_member['difference'])
            debit_member['difference'] += payment
            credit_member['difference'] -= payment
            payments.append({
                "sender": debit_member['name'],
                "receiver": credit_member['name'],
                "amount": float(-payment)
            })
    return payments

