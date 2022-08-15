# -----------------------------------------------------------------------
# modules
# -----------------------------------------------------------------------
# サードパーティ製
import freezegun

# Original
from pay import PayRecord, PayTable


# -----------------------------------------------------------------------
# Class
# -----------------------------------------------------------------------
class TestPayRecord:
    @freezegun.freeze_time('2022-6-6')
    def test_init(self):
        record = PayRecord('tomozo', 1000, '6/6 ハナマサで購入')
        assert record.__dict__ == {'Payer': 'tomozo', 'Amount': 1000, 'Memo': '6/6 ハナマサで購入', 'InputDate': '2022-06-06 09:00:00+09:00'}


class TestPayRepo:
    @freezegun.freeze_time('2022-6-6')
    def test_add_record_普通のレコード投入(self, local_dynamodb):
        table = PayTable()
        record = PayRecord('tomozo', 1000, '6/6 ハナマサで購入')
        response = table.add_record(record)

        assert response.status_code == 200
        assert response.body == {'Payer': 'tomozo', 'Amount': 1000, 'Memo': '6/6 ハナマサで購入', 'InputDate': '2022-06-06 09:00:00+09:00'}

    def test_add_record_レコード連続投入_InputDateだけ違うレコード(self, local_dynamodb):
        """
        InputDateが違うので、2件共正常に登録できる。
        """
        table = PayTable()
        record = PayRecord('tomozo', 1000, '6/6 ハナマサで購入')
        response = table.add_record(record)
        assert response.status_code == 200

        record2 = PayRecord('tomozo', 1000, '6/6 ハナマサで購入')
        response2 = table.add_record(record2)
        assert response2.status_code == 200

    def test_add_record_プライマリキーが被っているレコード連続投入(self, local_dynamodb):
        """
        プライマリキー(Payer and InputDate)被っているのでエラーになる。
        """
        table = PayTable()
        record = PayRecord('tomozo', 1000, '6/6 ハナマサで購入')
        response = table.add_record(record)
        response = table.add_record(record)

        assert response.status_code == 409
        assert response.body == {'message': 'レコードが重複しています。再度レコード登録を試してみてください。'}

    def test_get_amounts_レコードが0件(self, local_dynamodb):
        table = PayTable()
        response = table.get_amounts('tomozo')

        assert response.status_code == 200
        assert response.body == {'Payer': 'tomozo', 'Amounts': 0}

    def test_get_amounts_該当レコードが0件(self, local_dynamodb):
        """他人のレコードは存在する"""
        table = PayTable()

        record = PayRecord('taro', 500, 'ハナマサで購入')
        table.add_record(record)
        response = table.get_amounts('tomozo')

        assert response.status_code == 200
        assert response.body == {'Payer': 'tomozo', 'Amounts': 0}

    def test_get_amounts_該当レコードが1件(self, local_dynamodb):
        table = PayTable()
        record = PayRecord('tomozo', 1000, 'ハナマサで購入')
        table.add_record(record)

        # 他の人のレコードも投入しておく
        record = PayRecord('taro', 500, 'ハナマサで購入')
        table.add_record(record)

        # 総額取得
        response = table.get_amounts('tomozo')

        assert response.status_code == 200
        assert response.body == {'Payer': 'tomozo', 'Amounts': 1000}

    def test_get_amounts_該当レコードが複数件(self, local_dynamodb):
        """加算処理ができているかのテスト"""
        table = PayTable()
        record = PayRecord('tomozo', 1000, '6/6 ハナマサで購入')
        table.add_record(record)
        record2 = PayRecord('tomozo', 10111, '6/6 ハナマサで購入')
        table.add_record(record2)

        # 他の人のレコードも投入しておく
        record3 = PayRecord('taro', 500, '6/6 ハナマサで購入')
        table.add_record(record3)

        # 総額取得
        response = table.get_amounts('tomozo')

        assert response.status_code == 200
        assert response.body == {'Payer': 'tomozo', 'Amounts': 11111}
