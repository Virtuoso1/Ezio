import os
import requests
from dotenv import load_dotenv

load_dotenv()

class PesapalHandler:
    def __init__(self, consumer_key=None, consumer_secret=None, base_url=None, ipn_id=None):
        self.base_url = base_url or os.getenv("PESAPAL_BASE_URL", "https://cybqa.pesapal.com/pesapalv3")
        self.consumer_key = consumer_key or os.getenv("PESAPAL_CONSUMER_KEY")
        self.consumer_secret = consumer_secret or os.getenv("PESAPAL_CONSUMER_SECRET")
        self.ipn_id = ipn_id or os.getenv("PESAPAL_IPN_ID")

        if not self.consumer_key or not self.consumer_secret:
            raise ValueError("Pesapal Consumer Key and Secret must be provided or set in environment variables.")

    def _get_access_token(self):
        url = f"{self.base_url}/api/Auth/RequestToken"
        payload = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("token")
        else:
            raise Exception(f"Pesapal Authentication Failed: {response.text}")

    def register_ipn(self, notification_url):
        token = self._get_access_token()
        url = f"{self.base_url}/api/URLSetup/RegisterIPN"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = {
            "url": notification_url,
            "ipn_notification_type": "GET"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("ipn_id")
        else:
            raise Exception(f"Failed to register IPN: {response.text}")

    def initiate_payment(self, order_id, amount, description, callback_url, cancellation_url, billing_address):
    
        if not self.ipn_id:
            raise ValueError("Pesapal IPN ID is missing. Register one or set PESAPAL_IPN_ID in your .env file.")

        token = self._get_access_token()
        url = f"{self.base_url}/api/Transactions/SubmitOrderRequest"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "id": order_id,
            "currency": "KES",  
            "amount": amount,
            "description": description,
            "callback_url": callback_url,
            "cancellation_url": cancellation_url,
            "notification_id": self.ipn_id,
            "billing_address": billing_address
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to submit order: {response.text}")

    def get_transaction_status(self, order_tracking_id):
        token = self._get_access_token()
        url = f"{self.base_url}/api/Transactions/GetTransactionStatus?orderTrackingId={order_tracking_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch transaction status: {response.text}")