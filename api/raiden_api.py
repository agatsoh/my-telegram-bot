import requests


class RaidenApi:

    def __init__(self, raiden_api):
        self.raiden_api = f"{raiden_api}/api/v1"

    def payments(self, token_address, target_address, amount):
        url = f"{self.raiden_api}/payments/{token_address}/{target_address}"
        print(url)
        return requests.post(url,
                             headers={'Content-Type': 'application/json', },
                             json={'amount': amount})

    def getBalance(self, token_address, partner_address):
        url = f"{self.raiden_api}/channels/{token_address}/{partner_address}"
        print(url)
        return requests.get(url)
