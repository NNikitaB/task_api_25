from locust import HttpUser , task, between
import random
from uuid import uuid4

#POST api/v1/wallets/<WALLET_UUID>/operations


class WalletUser (HttpUser):
    wait_time = between(1, 3)  
    #pre task
    id:str


    def __init__(self):
        self.id = self.client.post("api/v2/wallets/create_wallet").json()["uuid"]


    @task
    def update_wallet(self):
        amount = random.randint(1, 100)
        # Define the payload for the wallet update
        payload1 = {
            "uuid": "DEPOSIT",
            "amount": amount,
        }
        payload2 = {
            "uuid": "WITHDRAW",
            "amount": amount,
        }
        payload = random.choice([payload1, payload2])
        # Send the update request to the API (replace '/update_wallet' with your actual endpoint)
        self.client.post("api/v1/wallets/{id}/operation".format(self.id), json=payload)

# To run Locust, you can specify the number of users and spawn rate in the command line.
# For example, to run with 100 users:
# locust -f locustfile.py --headless -u 100 -r 10 --host http://yourapi.com
