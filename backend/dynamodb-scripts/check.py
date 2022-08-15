# -----------------------------------------------------------------------
# import modules
# -----------------------------------------------------------------------
# サードパーティ製
import boto3

print('Check DynamoDB table.')
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
for tbl in dynamodb.tables.all():
    print(tbl.name)
