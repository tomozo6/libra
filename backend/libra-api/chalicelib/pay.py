# -----------------------------------------------------------------------
# modules
# -----------------------------------------------------------------------
from datetime import datetime, timedelta, timezone
import os

# サードパーティ製
import boto3
from chalice import Response
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from dataclasses import dataclass, field

# -----------------------------------------------------------------------
# Valiables
# -----------------------------------------------------------------------
content_type_json = {'Content-Type': 'application/json'}


# -----------------------------------------------------------------------
# Class
# -----------------------------------------------------------------------
@dataclass(frozen=True)
class PayRecord():
    """支払レコードクラス

    Attribures:
        Payer (str): 立替者
        Amount (int): 金額
        Memo (str): メモ
        InputDate (str): オブジェクトが生成された時間。生成時に動的に設定します。
    """
    Payer: str
    Amount: int
    Memo: str
    InputDate: str = field(init=False)

    def __post_init__(self):
        JST = timezone(timedelta(hours=9))
        object.__setattr__(self, 'InputDate', str(datetime.now(tz=JST)))


class PayTable():
    """支払テーブルクラス

    Attribures:
        table: boto3のdynamodbTableオブジェクト。

        dynamodbのエンドポイントとテーブル名は環境変数('DB_ENDPOINT_URL', 'PAY_TABLE_NAME')から取得します。
    """

    def __init__(self):
        endpoint = os.environ.get('DB_ENDPOINT_URL')
        table_name = os.environ.get('PAY_TABLE_NAME')

        if endpoint:
            dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint)
        else:
            dynamodb = boto3.resource('dynamodb')

        self.table = dynamodb.Table(table_name)


    def add_record(self, record: PayRecord) -> Response:
        """支払レコード登録

        Args:
            record (PayRecord): 支払レコードオブジェクト

        Returns:
            Response: chalice用Responseオブジェクトを返します
        """
        item = record.__dict__

        try:
            res = self.table.put_item(
                Item=item,
                ConditionExpression='attribute_not_exists(Payer) AND attribute_not_exists(InputDate)'
            )

            # if res['ResponseMetadata']['HTTPStatusCode'] == 200:
            #    return Response(
            #        body=record.__dict__,
            #        headers=content_type_json,
            #        status_code=200
            #    )
            return Response(
                body=record.__dict__,
                headers=content_type_json,
                status_code=200
            )

        except ClientError as e:
            print(e)
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return Response(
                    body={'message': 'レコードが重複しています。再度レコード登録を試してみてください。'},
                    headers=content_type_json,
                    status_code=409
                )

        except Exception as e:
            print(e)

    def get_amounts(self, payer: str) -> Response:
        """支払総額取得

        指定された支払者の総額を取得します。

        Args:
            payer (str): 支払者

        Returns:
            Response: chalice用Responseオブジェクトを返します
        """
        response = self.table.query(
            KeyConditionExpression=Key('Payer').eq(payer)
        )

        items = response['Items']
        amounts = sum(item.get('Amount', 0) for item in items)

        return Response(
            body={'Payer': payer, 'Amounts': amounts},
            headers=content_type_json,
            status_code=200
        )
