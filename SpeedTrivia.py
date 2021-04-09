# -*- coding: utf-8 -*-
"""SpeedTriva takes input from individual players via SMS using Twillio service.
Players can send their name by text and get back the names of their teammates.
Teams are "Randomly" assigned. 
This app tracks players from past events and strives to assign players together
that have not been at the same table before (like speed dating). 
Player can provide their personal name to the app and include a +1 (or +2 or more) 
to their name to reserve extra seats at their table.
FUNCTIONALITY:
    Incoming SMS;
        First ever incoming SMS becomes Control-Node.
            After that all new numbers are considered players.
                (Control is also player)
        Players can provide details like:
            Name, Team Size(are they alone or have brought partner(s)), 
            Whois (responds with names of other players assigned to table),
            Decline (Ask to be reassigned to different table),
            Team-Name (set it or ask for it), Name-suggestions (offer silly team name),
        Control can provide same as above, plus;
            Shuffle (re-shuffles players), Set-size (set the target size of each table),
            Table-list (returns list of all players and assignments),
            Send-Assignments (sends each player their tablename (e.g. epsilon, gamma, delta...)),

MINIMUM FUNCTIONALITY:
    Default table size equals 4.
    Incoming SMS is placed in the database and body of SMS is used as name and +n value.
        duplicate SMS phone numbers just updates the name and +n values.
    Control can Shuffle tables and send assignments to players.
    No stateful memory is needed between nights a this level.

CRAZY FUTURE FUNCTIONALITY:
    Player can provide the answer to the trivia question by SMS and SpeedTrivia will submit it 
    to the trivia host by filling in the jotform used for answers that night.

    Controller can provide actual answers for storage in the database and matching to the provided
    answers from the teams to keep score automatically within the app. (Alternately the player can
    tell SpeedTrivia when they get a question right so the score can be kept.)
"""



# Download the twilio-python library from twilio.com/docs/libraries/python
import sys
from cryptocode import decrypt
from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from loguru import logger
FILENAME = __file__
# Begin logging definition
logger.remove()  # removes the default console logger provided by Loguru.
# I find it to be too noisy with details more appropriate for file logging.

logger.add(
    "".join([FILENAME, "_{time}.log"]),
    rotation="Sunday",
    level="DEBUG",
    encoding="utf8"
)
# create a new log file for each run of the program


# Find these values at https://twilio.com/user/account
encrypted_account_sid = "vWFFuntfUAPQe/FTupv1OXV8AXWG5AaG8fzQp2ecunL7HA==*lmK4CGQhJTdlnZIJiVFmvQ==*DBCDTrmMz+oWPxgizpVkAA==*kaO0xIle1JPlQFS8syKmwQ=="
encrypted_auth_token = "LJ0ctrM7RN1N7JS2tIm5hvfVX+F85RQmb8pXpyxYE+g=*Z5nguaX60YPaM7zs2r//Ew==*EMZDFrrPZfZsWVoehWZEug==*33yCyWvj08vvbYliZcAVuQ=="
try:
    password = sys.argv[1]
except IndexError as e:
    print(f'Password not found. Please append password to commandline.')
    sys.exit(1)
account_sid = decrypt(encrypted_account_sid, password)
auth_token = decrypt(encrypted_auth_token, password)
client = Client(account_sid, auth_token)
TWILLIO_SMS_NUMBER = "+18122038235" # Paoli native number bought from Twilio


app = Flask(FILENAME)

# Basic test functionality roadmap:
#   Create a public facing Flask server.
#   Accept SMS messages, Place in local perm storage, reply to SMS with greeting.

@app.route("/sms", methods=["GET", "POST"])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    logger.debug('Message received. Strating response.')
    # Start our TwiML response
    resp = MessagingResponse()
    logger.debug(resp)
    # Add a message
    msg = "The Robots are coming! Head for the hills!"
    logger.debug(msg)
    resp.message(msg)
    logger.debug(str(resp))
    return str(resp)



if __name__ == "__main__":
    app.run(debug=True)
