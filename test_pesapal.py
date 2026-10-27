from pesapal import PesapalHandler

def run_test():
    print("Initializing Pesapal Handler...")
    pesapal = PesapalHandler()

    # Sample test order details
    order_id = "TEST-INV-2026-001"
    amount = 100.00  
    description = "Test Payment for Python Handler"
    
    # Placeholders for testing the redirect flow
    callback_url = "https://webhook.site/callback-test"
    cancellation_url = "https://webhook.site/cancel-test"
    
    billing_address = {
        "email_address": "testuser@example.com",
        "phone_number": "0712345678",
        "first_name": "Test",
        "last_name": "User",
        "country_code": "KE"
    }

    print(f"\nSubmitting test order '{order_id}' for KES {amount}...")
    try:
        response = pesapal.initiate_payment(
            order_id=order_id,
            amount=amount,
            description=description,
            callback_url=callback_url,
            cancellation_url=cancellation_url,
            billing_address=billing_address
        )

        print("\n--- Payment Successfully Initiated! ---")
        print(f"Order Tracking ID: {response.get('order_tracking_id')}")
        print(f"Merchant Reference: {response.get('merchant_reference')}")
        print(f"Redirect URL: {response.get('redirect_url')}")
        print("\n👉 Copy the Redirect URL above and paste it into your browser to complete a test payment.")
    
        tracking_id = response.get('order_tracking_id')
        if tracking_id:
            print(f"\nChecking initial status for tracking ID: {tracking_id}...")
            status_result = pesapal.get_transaction_status(tracking_id)
            print(f"Current Payment Status: {status_result.get('payment_status_description')}")

    except Exception as e:
        print(f"\nTest Failed with Error: {e}")

if __name__ == "__main__":
    run_test()