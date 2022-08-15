# -----------------------------------------------------------------------
# Modules
# -----------------------------------------------------------------------
# サードパーティ製
from chalice import Chalice

# Original
from chalicelib.pay import PayRecord, PayTable

# -----------------------------------------------------------------------
# 前処理
# -----------------------------------------------------------------------
app = Chalice(app_name='libra-api')


# -----------------------------------------------------------------------
# Routing
# -----------------------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    return {'hello': 'world'}


@app.route('/healthz', methods=['GET'])
def healthz():
    print()
    return {'msg': 'healthz ok.'}


@app.route('/pay/records', methods=['POST'])
def pay_records_post():
    repo = PayTable()
    request = app.current_request

    record = PayRecord(
        request.json_body['Payer'],
        request.json_body['Amount'],
        request.json_body['Memo']
    )

    return repo.add_record(record)
