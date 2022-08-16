# -----------------------------------------------------------------------
# Modules
# -----------------------------------------------------------------------
import json

# サードパーティ製
import freezegun


# -----------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------
def test_index(fixture_client):
    response = fixture_client.http.get('/')
    assert response.status_code == 200
    assert response.json_body == {'hello': 'world'}


def test_pay_recoreds_post(fixture_client, fixture_dynamodb):
    with freezegun.freeze_time('2022-06-06'):
        response = fixture_client.http.post(
            '/pay/records',
            headers={'Content-Type': 'application/json'},
            body=json.dumps({'Payer': 'tomozo', 'Amount': 1000, 'Memo': '6/6 ハナマサで購入'})
        )

    assert response.status_code == 200
    assert response.json_body == {'Payer': 'tomozo', 'Amount': 1000, 'Memo': '6/6 ハナマサで購入', 'InputDate': '2022-06-06 09:00:00+09:00'}
