# -*- coding: utf-8 -*-
TESTING = False

HELPFUL_INFO = """Welcome to SpeedTrivia. SpeedTrivia is designed to be a tool that
matches players with other players randomly. If you brought a favorite player with you
then simply reply to this number with the keyword 'plus'. You can add as many
seats as you need. Thanks for attending!
"""
TIME_INFO = """Trivia at Mac's Hideaway is Tuesday nights 
starting promptly at 7pm and runs 2 hours. """
WEBFORM_HELP = (
    """The website for entering your answers is: tinyurl.com/cemacshideaway"""
)
MOST_COMMON_HELP = """Common commands are add/remove plus ones. 
"Minus 1" removes 1. 
"Plus 2" adds 2 extra players.
"Status" tells you how many plus ones you have."""

import datetime as dt
import random
import time
from collections import defaultdict
from pathlib import Path
from pprint import pformat as pprint_dicts

import nltk
import pytz
from loguru import logger
from nltk.corpus.reader import propbank

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")
from nltk.corpus import stopwords

from ST_Twilio import Send_SMS

# begin definition of default dict keys for players
CALLERNAME = "Caller_name"
FIRSTCALL = "First_call"
RECENTCALL = "Recent_Call"
PLUS_ONES = "Plus_one"
PARTNER_HISTORY = "Partners_history"
MESSAGE_HISTORY = "Message_history"
CURRENT_TABLE_ASSIGNMENT = "Current_Table"
CURRENT_TEAM_NAME = "Current_team"


@logger.catch
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


FILENAME = "SpeedTrivia.py"
FILENAME_PATHOBJ = Path(__file__)
PROGRAM_START_TIME = dt.datetime.now(pytz.timezone("UTC"))

DATABASE_PATHOBJ = Path(f"{FILENAME}.db")
TABLESIZE = 3
CONTROLLER = "+18125577095"
FROZEN = False

tables = (
    list()
)  # A global list of table labels that is defined within the 'ShuffleTables' function
least_meetups = dict()  # A global that is defined within the 'ShuffleTables' function
TABLE_ASSIGNED = dict()  # A global that is defined within the 'ShuffleTables' function
# consisting of an entry for each player with the name of their table. (it has not been locked in during the shuffle process and gets locked in during the start function.)
TONIGHTS_PLAYERS = list()  # A global defined within the 'ShuffleTables' function

POSSIBLE_TEAM_NAMES = []
with open('team_names.txt', 'r') as fh:
    POSSIBLE_TEAM_NAMES = fh.readlines()

