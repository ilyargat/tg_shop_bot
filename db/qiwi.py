from httpx import Client
from db.db import del_token,token,give_balance
from config import TOKEN_QIWI,PHONE

def get(_id):
    client = Client()
    client.headers={"Accept":"application/json","Content-Type":"application/json","Authorization":"Bearer " + TOKEN_QIWI}

    parameters = {
        "rows": 1,
        "operation": "IN"
    }

    data = client.get(f"https://edge.qiwi.com/payment-history/v2/persons/{PHONE}/payments?", params = parameters,timeout=10).json()

    valid = token(_id)

    for payment in data['data']:
        if payment['comment'] == valid:
            give_balance(_id,int(payment['sum']['amount']))
            del_token(valid)
            return payment['sum']['amount']

