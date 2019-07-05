import urequests, json
from unixtime import unixtime
from settings import opennode_api_key


class LightningInvoice:

    expire_threshold_sec = 5 * 60
    http_headers = {
        'Content-Type': 'application/json',
        'Authorization': opennode_api_key
    }

    def __init__(self, id, payreq, expires_at):
        self.id = id
        self.payreq = payreq
        self.expires_at = expires_at

    @property
    def expired(self):
        return unixtime() > self.expires_at - self.expire_threshold_sec

    @property
    def paid(self):
        req = urequests.get('https://api.opennode.co/v1/charge/' + str(self.id), headers=self.http_headers)
        req_json = req.json()['data']
        if req_json['status'] == 'paid':
            return True
        return False

    @classmethod
    def gen_invoice(cls, priceSatoshis):
        assert isinstance(priceSatoshis, int)
        data = json.dumps({'amount': priceSatoshis})
        req = urequests.post('https://api.opennode.co/v1/charges', data=data, headers=cls.http_headers)
        req_json = req.json()
        return LightningInvoice(
            id=req_json['data']['id'],
            payreq=req_json['data']['lightning_invoice']['payreq'],
            expires_at=req_json['data']['lightning_invoice']['expires_at']
        )

