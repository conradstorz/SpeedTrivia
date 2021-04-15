"""Common constants and methods for SpeedTRIVIA."""
from loguru import logger
from pathlib import Path
from collections import defaultdict

# import Natural Language Toolkit.
import nltk
from nltk.corpus import stopwords
from nltk.corpus.reader import propbank
# verify nltk data downloads are up-to-date.
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")

# import our private repository of Twilio interface functions
import ST_twilio as tw

FILENAME = __file__
FILENAME_PATHOBJ = Path(__file__)

DATABASE_PATHOBJ = Path("".join([FILENAME, ".db"]))
TABLESIZE = 3
CONTROLLER = "+18125577095"
FROZEN = False
tables = list()  # A global list of table labels that is defined within the 'ShuffleTables' function
least_meetups = dict()  # A global that is defined within the 'ShuffleTables' function
TABLE_ASSIGNED = dict()  # A global that is defined within the 'ShuffleTables' function
# consisting of an entry for each player with the name of their table. (it has not been locked in during the shuffle process and gets locked in during the start function.)
TONIGHTS_PLAYERS = list()  # A global defined within the 'ShuffleTables' function


# begin definition of default dict keys for players
CALLERNAME = "Caller_name"
FIRSTCALL = "First_call"
RECENTCALL = "Recent_Call"
PLUS_ONES = "Plus_one"
PARTNER_HISTORY = "Partners_history"
MESSAGE_HISTORY = "Message_history"
CURRENT_TABLE_ASSIGNMENT = "Current_Table"
CURRENT_TEAM_NAME = "Current_team"


def dict_default():
    sample_player_dict = {
        CALLERNAME: "",
        CURRENT_TABLE_ASSIGNMENT: "Undefined",
        CURRENT_TEAM_NAME: "notset",
        PLUS_ONES: int(0),  # represents number of extra seats reserved at the table
        PARTNER_HISTORY: [],
        MESSAGE_HISTORY: [],
        FIRSTCALL: None,
        RECENTCALL: None,
    }
    return sample_player_dict


players_database = defaultdict(dict_default)
players_database["root"] = "root"


def ask_caller_their_name():
    logger.info("Asking the caller their name.")
    return "Hello! I don't have your number in my records. Could you please tell me your name?"


def ProperNounExtractor(text):
    # if text is only a single word, like 'Doug', this routine does not identify it as a name.
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        words = [word for word in words if word not in set(stopwords.words("english"))]
        tagged = nltk.pos_tag(words)
        for (word, tag) in tagged:
            if tag == "NNP":  # If the word is a proper noun
                return word
    return None


def check_sms_for_name(msid, sms_from, body_of_sms):
    # Function to extract the proper names from free form text.
    global CONTROLLER, players_database, CALLERNAME
    logger.info("Searching the sms for the callers name.")
    callername = ProperNounExtractor(body_of_sms)
    if callername != None:
        logger.info("Found a name:")
        logger.info(callername)
        tw.Send_SMS("".join(["New Caller is: ", callername]), CONTROLLER)
        players_database[sms_from][CALLERNAME] = callername
    else:
        logger.info("Couldn't find a name.")
        return "Sorry. I didn't understand.  Please try again. Feel free to speak in full sentences."
    return "".join(
        ["Thanks ", callername, "! Glad to meet you. Welcome to SpeedTrivia."]
    )


