# -----------------------------------------------------------------------
# Modules
# -----------------------------------------------------------------------
import json

# サードパーティ製
import freezegun


# -----------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------
def test_index(test_client):
    response = test_client.http.get('/')
    assert response.status_code == 200
    assert response.json_body == {'hello': 'world'}


def test_pay_recoreds_post(test_client, local_dynamodb):
    with freezegun.freeze_time('2022-06-06'):
        response = test_client.http.post(
            '/pay/records',
            headers={'Content-Type': 'application/json'},
            body=json.dumps({'Payer': 'tomozo', 'Amount': 1000, 'Memo': '6/6 ハナマサで購入'})
        )

    assert response.status_code == 200
    assert response.json_body == {'Payer': 'tomozo', 'Amount': 1000, 'Memo': '6/6 ハナマサで購入', 'InputDate': '2022-06-06 09:00:00+09:00'}
