"""Common constants and methods for SpeedTRIVIA."""
from loguru import logger
from pathlib import Path
import random
import time
from collections import defaultdict
import pytz
import datetime as dt
from pprint import pformat as pprint_dicts

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
tables = (
    list()
)  # A global list of table labels that is defined within the 'ShuffleTables' function
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


def how_long_ago_is(past_time):
    delta_ = dt.datetime.now(pytz.timezone("UTC")) - past_time
    days_ = delta_ / dt.timedelta(days=1)
    logger.debug("".join(["Time since ", str(days_)]))
    return days_


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


def AddReservation(msid, sms_from, body_of_sms):
    """Add a +1 to this players table."""
    logger.info("Add a plue one function entered.")
    items = body_of_sms.split()
    try:
        number = int(items[1])
    except ValueError as e:
        number = 1
    players_database[sms_from][PLUS_ONES] += number
    return f"You now have {str(players_database[sms_from][PLUS_ONES] + 1)} reserved seats at your table counting yourself."


def RemoveReservation(msid, sms_from, body_of_sms):
    """Players can reserve extra seats at their table for special guests.
    Those guests don't register with this app on their own they just sit
    at the same table by design. (e.g. a non-player or spouse.)
    """
    logger.info("Remove a plus one from player function entered.")
    items = body_of_sms.split()
    try:
        number = int(items[1])
    except ValueError as e:
        number = 1
    if (players_database[sms_from][PLUS_ONES] - number) >= 0:
        players_database[sms_from][PLUS_ONES] -= number
    else:
        players_database[sms_from][PLUS_ONES] = 0
    return f"You now have {str(players_database[sms_from][PLUS_ONES] + 1)} reserved seats at your table counting yourself."

def ReturnTableName(msid, sms_from, body_of_sms):
    """Table name is an index value. (e.g. Gamma, delta, epsilon...)"""
    logger.info("return player team table label function entered.")
    return "".join(
        ["Your table is ", players_database[sms_from][CURRENT_TABLE_ASSIGNMENT], "."]
    )


def SetTeamName(msid, sms_from, body_of_sms):
    """Team name is the formal name. (e.g. 'Fools for the Trivia')
    When entered for one player applies for all at table.
    """
    logger.info("Set team name function entered.")
    return msid


def list_players_in_database(tonight=False):
    tp_list = []
    for k in players_database.keys():
        if len(k) == 12:  # ignore entries that are not phone numbers
            # Entries that are not phone numbers are system variables for internal use.
            # TODO this could be made more robust with a regex ('+1dddddddddd')
            dlta = how_long_ago_is(players_database[k][RECENTCALL])
            if tonight:  # Filter out records from past weeks if tonight equal True.
                if dlta < 6:
                    tp_list.append(k)
            else:
                tp_list.append(k)
    return tp_list


def Tonights_players():
    return list_players_in_database(tonight=True)


def ReturnStatus(msid, sms_from, body_of_sms):
    """Return various details of this player."""
    logger.info("Send status to player function entered.")
    stat = f"{players_database[sms_from][CALLERNAME]} your table name is {players_database[sms_from][CURRENT_TABLE_ASSIGNMENT]} and you have {str(players_database[sms_from][PLUS_ONES])}"           " extra seats reserved.",
    if sms_from == CONTROLLER:  # include extra information.
        stat = f"{stat} --status: {str(TABLESIZE)} per table. {str(len(Tonights_players()))} players registered for tonight. {str(tables)}"
    return stat


def SuggestFunny(msid, sms_from, body_of_sms):
    """Return some ideas for team names."""
    logger.info("Funny team name suggestions entered.")
    return msid


def SuggestSerious(msid, sms_from, body_of_sms):
    """Suggest only serious names."""
    logger.info("Serious team name suggestions entered.")
    return msid


def ChangePlayerName(msid, sms_from, body_of_sms):
    """Allow player to correct their own name."""
    logger.info("Change players name function entered.")
    callername = ProperNounExtractor(body_of_sms)
    if callername != None:
        players_database[sms_from][CALLERNAME] = callername
        reply = "".join(["Thanks ", callername, "! Your name has been updated."])
    else:
        reply = "Sorry, I did not understand."
    return reply


def ChangeTeamName(msid, sms_from, body_of_sms):
    """Allow player to change the name of their team.
    This will work best after the night has been started
    and the table assignments have been set. This functionality
    is only useful for automated game answers processing.
    """
    logger.info("Change team name function entered.")
    return msid


def ShuffleTables(msid, sms_from, body_of_sms):
    """Primary function of this app is to match players to tables.
    This function 'randomly' assigns players to tables taking into account
    the max table size, the plus ones,  and players that have previously played together.
    Shuffle will try repeatedly to find a solution that exposes the maximum number of
    players to players that they have not played against before.
    """
    global least_meetups, TONIGHTS_PLAYERS, TABLE_ASSIGNED, tables

    def extra_players(player_list):
        plus_ones = 0
        for player in player_list:  # Find all the extra players in this list.
            plus_ones += players_database[player][PLUS_ONES]
        logger.debug("".join([str(plus_ones), " Extra players"]))
        return plus_ones

    def open_chairs(table):
        open_chrs = TABLESIZE - (len(table) + extra_players(table))
        logger.debug("".join([str(open_chrs), " Open chairs."]))
        if open_chrs < 1:
            return 0
        return open_chrs

    def Assign_Tables(tables, players):
        tbl_dict = defaultdict(list)
        for player in players:
            while player != None:
                rnd_table = random.choice(tables)
                logger.debug("".join([str(rnd_table), " random table."]))
                if open_chairs(tbl_dict[rnd_table]) > 0:
                    tbl_dict[rnd_table].append(player)
                    logger.debug("".join([player, " assigned to table."]))
                    player = None
        return tbl_dict

    # Begin ShuffleTables:
    logger.info("Shuffle players function entered.")
    TABLE_NAMES = [
        "gamma",
        "epsilon",
        "delta",
        "alpha",
        "kappa",
        "sigma",
        "beta",
        "theta",
    ]
    TONIGHTS_PLAYERS = Tonights_players()
    logger.debug(f"{str(TONIGHTS_PLAYERS)} Tonights players.")
    TOT_PLAYERS = len(TONIGHTS_PLAYERS) + extra_players(TONIGHTS_PLAYERS)
    logger.debug("".join([str(TOT_PLAYERS), " Total players."]))
    NUM_OF_TABLES = int(TOT_PLAYERS / TABLESIZE) + 1
    if NUM_OF_TABLES < 1:
        NUM_OF_TABLES = 1
    tables = TABLE_NAMES[:NUM_OF_TABLES]
    logger.debug("".join([str(tables), " Tonights tables."]))

    def Proposed_assignments():
        proposed_tables = Assign_Tables(tables, TONIGHTS_PLAYERS)
        logger.info(pprint_dicts(proposed_tables))
        return proposed_tables

    def Total_number_of_meetups(table_dict):
        """Return a total number of times any player has played against
        any other player at their table.
        """
        Total_collisions = 0
        # loop through tables
        logger.debug(pprint_dicts(table_dict))
        for table in table_dict.keys():
            table_collisions = 0
            logger.debug(str(table))
            # loop through players at that table
            for player in table_dict[table]:
                logger.debug(player)
                # look at their history for players at their table tonight.
                for prev in players_database[player][PARTNER_HISTORY]:
                    if prev in table_dict[table]:
                        table_collisions += 1
                        Total_collisions += 1
                        # increment the total counter for each collision
            logger.debug("".join(["Table collisions: ", str(table_collisions)]))
        logger.debug("".join(["Player collisions: ", str(Total_collisions)]))
        return Total_collisions

    NUMBER_OF_GUESSES = len(TONIGHTS_PLAYERS)
    guesses = dict()
    for itr in range(NUMBER_OF_GUESSES):
        guesses[itr] = Proposed_assignments()
        logger.debug("".join(["Guess ", str(itr), " is ", pprint_dicts(guesses[itr])]))
    least_meetups = dict()
    meets = 80000
    for guess in guesses.keys():
        logger.debug("".join(["Calculating past meetups for proposal: ", str(guess)]))
        tnom = Total_number_of_meetups(guesses[guess])
        if meets > tnom:
            meets = tnom
            least_meetups = guesses[guess]
    logger.debug("".join(["Most unique tables are: ", pprint_dicts(least_meetups)]))
    for table in least_meetups.keys():
        for player in least_meetups[table]:
            TABLE_ASSIGNED[player] = table
    # final number of tables may be less than original estimation so re-establish
    tables = least_meetups.keys()
    return "Players have been assigned tables."


def StartGame(msid, sms_from, body_of_sms):
    """Locks-in the table assignments and updates each player's database to record
    the event of these players being at the same table.
    """
    logger.info("Start game night function entered.")
    logger.debug(pprint_dicts(TABLE_ASSIGNED))
    for player in TONIGHTS_PLAYERS:
        logger.debug(player)
        # set players tablename
        players_database[player][CURRENT_TABLE_ASSIGNMENT] = TABLE_ASSIGNED[player]
        # Notify players by text of their table assignments.
        """Send_SMS(
            f"SpeedTrivia suggests you sit at table: {TABLE_ASSIGNED[player]}",
            player
        )"""
        logger.info(f"SpeedTrivia suggests you sit at table: {TABLE_ASSIGNED[player]}")

        time.sleep(2)
        # add other players from table to history list
        for teammate in least_meetups[TABLE_ASSIGNED[player]]:
            if teammate == player:
                pass
            else:
                logger.debug(f"Adding :{teammate} to {player}")
                players_database[player][PARTNER_HISTORY].append(teammate)
                # TODO consider if this should be a database with teammates and dates.
                # for now it just a list with duplicates.
    return "Players have been notified."


def ChangeTeamSize(msid, sms_from, body_of_sms):
    """Sets the maximum target size for tables.
    Due to players having +1's some tables could go over this limit.
    Generaly that will only happen if a team wants to have more +1's than
    the normal table size.
    """
    global TABLESIZE  # needed because I want to change the global value
    logger.info("Change team size function entered.")
    parts = str(body_of_sms).split()
    number = 0
    for part in parts:
        try:
            number = int(part)
        except:
            pass
    if number > 0:
        TABLESIZE = number
    else:
        return "Error. New table size not understood."
    return f"New table size = {str(TABLESIZE)}"


def Send_Announcement(msid, sms_from, body_of_sms):
    """Send an SMS to ALL registered players."""
    # Remove the keyword 'Announcement' from the body_of_sms before sending.
    announcement = body_of_sms
    for player in list_players_in_database():
        #  Attach the disclaimer instructions on how to STOP texts
        tw.Send_SMS(announcement, player)
    return


def Send_players_list(msid, sms_from, body_of_sms):
    """Send an SMS to CONTROLLER of ALL registered players."""
    for player in list_players_in_database():
        #  Attach the disclaimer instructions on how to STOP texts
        tw.Send_SMS(
            f"{players_database[player][CALLERNAME]} has {str(players_database[player][PLUS_ONES])}", 
            CONTROLLER
        )
        logger.debug(
            f"Player: {players_database[player][CALLERNAME]} has {str(players_database[player][PLUS_ONES])} extra seats."
        )
