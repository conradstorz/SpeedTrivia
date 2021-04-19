from collections import defaultdict
from loguru import logger
from pprint import pformat as pprint_dicts
from pathlib import Path

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

DATABASE_PATHOBJ = Path("SpeedTrivia.py.db")

# Save a dictionary into a pickle file.
import pickle

if DATABASE_PATHOBJ.exists():
    logger.info("Recovering pickle database...")
    players_database = pickle.load(open(DATABASE_PATHOBJ, "rb"))
else:
    logger.info("Creating new pickle database...")
    pickle.dump(players_database, open(DATABASE_PATHOBJ, "wb"))

print(pprint_dicts(players_database))
