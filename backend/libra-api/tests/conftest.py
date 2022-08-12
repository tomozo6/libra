# -----------------------------------------------------------------------
# import modules
# -----------------------------------------------------------------------
# サードパーティ製
import boto3
from chalice.test import Client
from pytest import fixture
import os

# 自作
from app import app


# -----------------------------------------------------------------------
# Fixture
# -----------------------------------------------------------------------
@fixture
def test_client():
    with Client(app) as client:
        yield client


@fixture
def local_dynamodb():
    # 環境変数の設定
    db_endpoint_url = 'http://localhost:8000'
    os.environ['DB_ENDPOINT_URL'] = 'http://localhost:8000'

    pay_table_name = 'libra-test-table'
    os.environ['PAY_TABLE_NAME'] = pay_table_name

    # DynamoDBの支払テーブルの作成
    dynamodb = boto3.resource('dynamodb', endpoint_url=db_endpoint_url)
    table_name = pay_table_name

    dynamodb.create_table(
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

    yield dynamodb

    # DynamoDBの支払テーブルを削除
    dynamodb.Table(table_name).delete()
