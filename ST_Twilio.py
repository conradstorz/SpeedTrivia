# -*- coding: utf-8 -*-

import os
import sys
from loguru import logger
from ST_common import *
from twilio.rest import Client
# from twilio.twiml.messaging_response import MessagingResponse

# Twilio token setup: 
CLIENT = None
if not os.system("set ACCOUNT_SID"):  # are these return values inverted?
    logger.info("Twilio ACCOUNT_SID found.")
    if not os.system(
        "set AUTH_TOKEN"
    ):  # seems like they would be true if the value exists.
        logger.info("Twilio AUTH_TOKEN found, registering Twilio Client...")
        ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
        AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
        CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)
        logger.info("Client token created:")
        logger.info(CLIENT)
if CLIENT == None:
    print("Client token not set. Did you load the environment variables?")
    print("Did you re-start VScode?")
    sys.exit(1)
    

@logger.catch
def Send_SMS(text, receipient):
    # TODO place a block on SMS between 10pm and 8am
    logger.info(f"Sending: '{text}' :->to->: {receipient}")
    CLIENT.messages.create(body=text, from_=TWILLIO_SMS_NUMBER, to=receipient)
    return
