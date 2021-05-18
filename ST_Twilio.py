# -*- coding: utf-8 -*-

import os
import sys

from loguru import logger
from twilio.rest import Client

TWILLIO_SMS_NUMBER = "+18122038235"  # Paoli native number bought from Twilio

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

def Is_Valid(number):
    """Validate correct format for USA cellphone. Also 
        check time of day at recipient by area-code and block messages 
        after 10PM and before 8am.
    Args:
        number (str): Valid SMS number
    Returns:
        bool: True if SMS can be sent.
    """
    if len(number) == 12:
        if type(number) == str:
            return True


@logger.catch
def Send_SMS(text, receipient):
    # TODO place a block on SMS between 10pm and 8am
    logger.info(f"Sending: '{text}' :->to->: {receipient}")
    if (type(text) is str) and (len(text) >  0) and (len(text) < 420):
        if Is_Valid(receipient):
            CLIENT.messages.create(body=text, from_=TWILLIO_SMS_NUMBER, to=receipient)
            logger.debug('Message sent.')  # Mostly this entry is for timestamping the Twilio process time.
        else:
            logger.error(f'Destination not valid: {receipient} no message sent.')
    else:
        logger.error(f'Message is not valid or too long: {text}')
    return
