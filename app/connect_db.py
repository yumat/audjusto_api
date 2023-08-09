import boto3

# ddb = boto3.resource('dynamodb')
ddb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000",
                            region_name='us-west-2',
                            aws_access_key_id='ACCESS_ID',
                            aws_secret_access_key='ACCESS_KEY')
group_table = ddb.Table("group_table")
members_table = ddb.Table("members_table")
pay_table = ddb.Table("payhistory_table")