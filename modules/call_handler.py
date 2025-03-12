from twilio.rest import Client
import time
from .google_sheets import update_call_status, update_customer_response

from modules.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER



client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def make_call(customer_name, phone_number, loan_amount, due_date, row_number):
    """
    Make an automated call to the customer and track call status and response.
    """
    if not phone_number.startswith("+"):
        phone_number = "+91" + phone_number  # ✅ Ensure proper international format

    message = f"""
    Hello {customer_name}, this is an automated reminder. Your loan of {loan_amount} is due on {due_date}. 
    Press 1 to acknowledge or 2 to request a callback. Thank you.
    """

    call = client.calls.create(
        twiml=f"""
        <Response>
            <Gather numDigits="1" action="https://your-server.com/handle-response?row={row_number}" method="POST">
                <Say>{message}</Say>
            </Gather>
        </Response>
        """,
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER
    )

    print(f"Call placed to {customer_name} at {phone_number}. Call SID: {call.sid}")

    time.sleep(10)  

    call_status = client.calls(call.sid).fetch().status
    update_call_status(row_number, call_status)
