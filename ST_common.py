"""Common constants and methods for SpeedTRIVIA."""
from loguru import logger


def ask_caller_their_name():
    logger.info("Asking the caller their name.")
    return "Hello! I don't have your number in my records. Could you please tell me your name?"



def check_sms_for_name(msid, sms_from, body_of_sms):
    # Function to extract the proper names from free form text.
    logger.info("Searching the sms for the callers name.")
    callername = ProperNounExtractor(body_of_sms)
    if callername != None:
        logger.info("Found a name:")
        logger.info(callername)
        Send_SMS("".join(["New Caller is: ", callername]), CONTROLLER)
        players_database[sms_from][CALLERNAME] = callername
    else:
        logger.info("Couldn't find a name.")
        return "Sorry. I didn't understand.  Please try again. Feel free to speak in full sentences."
    return "".join(
        ["Thanks ", callername, "! Glad to meet you. Welcome to SpeedTrivia."]
    )


