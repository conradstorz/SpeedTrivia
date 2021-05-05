# Save a dictionary into a pickle file.
import pickle  # TODO put all of pickle code into seperate .py file and import
from collections import defaultdict
from pathlib import Path
from pprint import pformat as pprint_dicts

from loguru import logger

from ST_common import *

# export commands GetDB() and PutDB()

print(DATABASE_PATHOBJ.name)
if DATABASE_PATHOBJ.exists():
    logger.info("Recovering pickle database...")
    players_database = pickle.load(open(DATABASE_PATHOBJ, "rb"))
else:
    logger.info("Creating new pickle database...")
    pickle.dump(players_database, open(DATABASE_PATHOBJ, "wb"))


print(pprint_dicts(players_database))
