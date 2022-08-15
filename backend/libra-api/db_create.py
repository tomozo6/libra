# -----------------------------------------------------------------------
# import modules
# -----------------------------------------------------------------------
# サードパーティ製
import boto3

print('Create DynamoDB table.')
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

table_name = 'tttest_table'

res = dynamodb.create_table(
    BillingMode='PAY_PER_REQUEST',
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': 'Payer',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'InputDate',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'Payer',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'InputDate',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)

print(res)
