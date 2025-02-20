from locust import HttpUser , task, between,events
import random
from uuid import uuid4
import requests
#POST api/v1/wallets/<WALLET_UUID>/operations
id:str
host = "http://fastapi:8080/"
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("A new test is starting")
    global id
    response = requests.post(host+"api/v2/wallet/create")
    if response.status_code == 200:
        id = response.json().get("uuid")
    else:
        id = ""
@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("A test has ended")
    global id
    response = requests.post(host+f"api/v2/wallet/delete?uuid={id}")

class WalletUser (HttpUser):
    wait_time = between(1, 3)  
    #pre task

    #save id before request


    def on_start(self):
        global id
        self.id = id

    @task(90)
    def update_wallet(self):
        amount = random.randint(1, 1000)
        # Define the payload for the wallet update
        payload1 = {
            "operationType": "DEPOSIT",
            "amount": amount,
        }
        payload2 = {
            "operationType": "WITHDRAW",
            "amount": amount,
        }
        payload = random.choice([payload1, payload2])
        # Send the update request to the API (replace '/update_wallet' with your actual endpoint)
        self.client.post(host+"api/v1/wallets/{0}/operation".format(self.id), json=payload)
    @task(10)
    def get_wallet(self):
        self.client.get(host+"api/v1/wallets/{0}".format(self.id))

# To run Locust, you can specify the number of users and spawn rate in the command line.
# For example, to run with 100 users:
# locust -f locustfile.py --headless -u 100 -r 10 --host http://yourapi.com
