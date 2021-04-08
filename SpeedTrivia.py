# -*- coding: utf-8 -*-
"""SpeedTriva takes input from individual players via SMS using Twillio service.
Players can send their name by text and get back the names of their teammates.
Teams are "Randomly" assigned. This app tracks players from past events and strives
to assign players together that have not been at the same table before.
"""



# Download the twilio-python library from twilio.com/docs/libraries/python
import sys
from cryptocode import decrypt
from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse



password = sys.argv[1]
# Find these values at https://twilio.com/user/account
encrypted_account_sid = "vWFFuntfUAPQe/FTupv1OXV8AXWG5AaG8fzQp2ecunL7HA==*lmK4CGQhJTdlnZIJiVFmvQ==*DBCDTrmMz+oWPxgizpVkAA==*kaO0xIle1JPlQFS8syKmwQ=="
encrypted_auth_token = "LJ0ctrM7RN1N7JS2tIm5hvfVX+F85RQmb8pXpyxYE+g=*Z5nguaX60YPaM7zs2r//Ew==*EMZDFrrPZfZsWVoehWZEug==*33yCyWvj08vvbYliZcAVuQ=="
password = sys.argv[1]
account_sid = decrypt(encrypted_account_sid, password)
auth_token = decrypt(encrypted_auth_token, password)
client = Client(account_sid, auth_token)
TWILLIO_SMS_NUMBER = "+15555555555"



def sms_send(target_number="+12316851234", message="Hello there!"):
    client.api.account.messages.create(
        to=target_number, from_=TWILLIO_SMS_NUMBER, body=message
    )
    return True



app = Flask(__name__)



@app.route("/sms", methods=["GET", "POST"])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()
    # Add a message
    resp.message("The Robots are coming! Head for the hills!")
    return str(resp)



if __name__ == "__main__":
    app.run(debug=True)
