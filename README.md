# Ezio
Pesapal Python Payment Handler (API 3.0)

A lightweight, plug and play Python handler for integrating **Pesapal API 3.0 (JSON)**. This package abstracts away the complexities of token generation, IPN management, and payload formatting, letting you initiate payments and check statuses with single function calls.

---

## Project Structure

```text
your-project-folder/
├── pesapal.py        # Core PesapalHandler class module
├── test_pesapal.py   # Example script to test the payment flow
└── .env              # Environment variables & credentials (sandbox credentials)
```

---

## Prerequisites & Installation

1. Make sure you have Python installed.
2. Install the required dependencies (`requests` and `python-dotenv`):
   ```bash
   pip install requests python-dotenv
   ```

---

## Configuration (`.env`)

Edit the `.env` file in the root directory of your project to store your sandbox credentials and registered IPN ID safely out of your source code:

```env
# Pesapal API 3.0 Sandbox Configuration
PESAPAL_BASE_URL=https://cybqa.pesapal.com/pesapalv3
PESAPAL_CONSUMER_KEY=your_sandbox_consumer_key_here
PESAPAL_CONSUMER_SECRET=your_sandbox_consumer_secret_here
PESAPAL_IPN_ID=your_registered_ipn_id_here
```

---

## 🚀 How to Implement It in Your App

You can easily import the `PesapalHandler` class into any part of your application (Flask, FastAPI, Django, or standard scripts) and process payments with minimal arguments:

```python
from pesapal import PesapalHandler

# Initialize the handler (automatically loads credentials & IPN from .env)
pesapal = PesapalHandler()

try:
    payment_response = pesapal.initiate_payment(
        order_id="INV-2026-001",
        amount=1500.00,
        description="Subscription Payment",
        callback_url="https://yourdomain.com/payment-complete",
        cancellation_url="https://yourdomain.com/payment-cancelled",
        billing_address={
            "email_address": "johndoe@example.com",
            "phone_number": "0712345678",
            "first_name": "John",
            "last_name": "Doe",
            "country_code": "KE"
        }
    )

    redirect_url = payment_response.get("redirect_url")
    tracking_id = payment_response.get("order_tracking_id")
    
    print(f"Redirect user to: {redirect_url}")

except Exception as e:
    print(f"Payment initiation failed: {e}")
```

---

## 🧪 Running the Example (`test_pesapal.py`)

The `test_pesapal.py` script serves as a complete **working example** to demonstrate how to call the handler, submit a sample test order, and verify transaction statuses.

To run the test:
```bash
python test_pesapal.py
```

### What `test_pesapal.py` does:
1. Instantiates `PesapalHandler`.
2. Automatically generates a Bearer token behind the scenes.
3. Submits a test order for **100 KES**.
4. Prints out the **Redirect URL** (which you can open in your browser to simulate paying in the Pesapal sandbox).
5. Queries the initial status using the generated `order_tracking_id`.