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

# NOTE: On 4-8-2021 I decided to use PythonAnywhere.com to host this code. 
    It can be accessed at Conradical.pythonanywhere.com/sms
    Twilio.com sends incoming texts from the number (812)203-8235 to the address above.
    The resulting string generated by sms_reply() is then returned to the player.
    An empty string from sms_reply() returns nothing and generates no return text.
    At this time I do not use environment variables at PA.com
    I simply cut and paste the un-encrypted secrets into the code at PA.com
    That code doesn't get pushed to GIT ever so the secrets are fairly safe.

# NOTE: Reading the Twilio website I learned about ngrok.exe
    ngrok is available for all computer platforms and creates tunnels from localhost to the public internet.
    Using ngrok allows testing servers like flask running on localhost with internet resources like Twilio.
    During developement of a webapp like SpeedTriva ngrok allows me to point Twilio at my localhost for testing.
    Deployment to production can then point Twilio back to Conradical.pythonAnywhere.com 
    
"""
HELPFUL_INFO = """Welcome to SpeedTrivia. SpeedTrivia is designed to be a tool that
matches players with other players randomly. If you brought a favorite player with you
then simply reply to this number with 'Add a plus one to my table'. You can add as many
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
# Download the twilio-python library from twilio.com/docs/libraries/python
import os
import sys
import time
from nltk.corpus.reader import propbank
from twilio.rest import Client
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from loguru import logger
from pprint import pformat as pprint_dicts
import datetime as dt
from pathlib import Path
import pytz
import nltk

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")
from nltk.corpus import stopwords
from collections import defaultdict
import random

FILENAME = __file__
FILENAME_PATHOBJ = Path(__file__)
PROGRAM_START_TIME = dt.datetime.now(pytz.timezone("UTC"))


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


def how_long_ago_is(past_time):
    delta_ = dt.datetime.now(pytz.timezone("UTC")) - past_time
    days_ = delta_ / dt.timedelta(days=1)
    logger.debug("".join(["Time since ", str(days_)]))
    return days_


TWILLIO_SMS_NUMBER = "+18122038235"  # Paoli native number bought from Twilio
DATABASE_PATHOBJ = Path("".join([FILENAME, ".db"]))
TABLESIZE = 3
CONTROLLER = "+18125577095"
FROZEN = False
least_meetups = dict()  # A global that is defined within the 'ShuffleTables' function
TABLE_ASSIGNED = dict()  # A global that is defined within the 'ShuffleTables' function
# consisting of an entry for each player with the name of their table. (it has not been locked in during the shuffle process and gets locked in during the start function.)
TONIGHTS_PLAYERS = list()  # A global defined within the 'ShuffleTables' function

# Begin logging definition
logger.remove()  # removes the default console logger provided by Loguru.
# I find it to be too noisy with details more appropriate for file logging.
# create a new log file for each run of the program
logger.add(
    "".join([FILENAME, "_{time}.log"]),
    rotation="Sunday",
    level="DEBUG",
    encoding="utf8",
)
# end logging setup
logger.info("Program started.")

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


def ReturnCommandList(msid, sms_from, body_of_sms):
    return str(COMMANDS.keys())


def AddReservation(msid, sms_from, body_of_sms):
    """Add a +1 to this players table."""
    logger.info("Add a plue one function entered.")
    items = body_of_sms.split()
    try:
        number = int(items[1])
    except ValueError as e:
        number = 1
    players_database[sms_from][PLUS_ONES] += number
    return "".join(
        [
            "You now have ",
            str(players_database[sms_from][PLUS_ONES] + 1),
            " reserved seats at your table counting yourself.",
        ]
    )


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
    return "".join(
        [
            "You now have ",
            str(players_database[sms_from][PLUS_ONES] + 1),
            " reserved seats at your table counting yourself.",
        ]
    )


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
    stat = "".join(
        [
            players_database[sms_from][CALLERNAME],
            " your table name is ",
            players_database[sms_from][CURRENT_TABLE_ASSIGNMENT],
            " and you have ",
            str(players_database[sms_from][PLUS_ONES]),
            " extra seats reserved.",
        ]
    )
    if sms_from == CONTROLLER:
        stat = "".join(
            [
                stat,
                " --status: ",
                str(TABLESIZE),
                " per table. ",
                str(len(Tonights_players())),
                " players registered for tonight.",
            ]
        )
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


def ReturnHelpInfo(msid, sms_from, body_of_sms):
    """Returns basic info about this app and the trivia competition."""
    logger.info("Help info function entered.")
    return HELPFUL_INFO


def ShuffleTables(msid, sms_from, body_of_sms):
    """Primary function of this app is to match players to tables.
    This function 'randomly' assigns players to tables taking into account
    the max table size, the plus ones,  and players that have previously played together.
    Shuffle will try repeatedly to find a solution that exposes the maximum number of
    players to players that they have not played against before.
    """
    global least_meetups, TONIGHTS_PLAYERS, TABLE_ASSIGNED

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
    logger.debug(
        "".join(
            [
                str(TONIGHTS_PLAYERS),
                " Tonights players.",
            ]
        )
    )
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
            "".join(
                ["SpeedTrivia suggests you sit at table: ", TABLE_ASSIGNED[player]]
            ),
            player,
        )"""
        logger.info(
            "".join(["SpeedTrivia suggests you sit at table: ", TABLE_ASSIGNED[player]])
        )
        time.sleep(2)
        # add other players from table to history list
        for teammate in least_meetups[TABLE_ASSIGNED[player]]:
            if teammate == player:
                pass
            else:
                logger.debug("".join(["Adding :", teammate, " to ", player]))
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
    return "".join(["New table size = ", str(TABLESIZE)])


def Send_Announcement(msid, sms_from, body_of_sms):
    """Send an SMS to ALL registered players."""
    # Remove the keyword 'Announcement' from the body_of_sms before sending.
    announcement = body_of_sms
    for player in list_players_in_database():
        #  Attach the disclaimer instructions on how to STOP texts
        Send_SMS(announcement, player)
    return


def Send_common_commands_help(msid, sms_from, body_of_sms):
    logger.debug(
        "".join(
            ["User: ", players_database[sms_from][CALLERNAME], " asked for Form-Help."]
        )
    )
    return MOST_COMMON_HELP


def Send_Webform_help(msid, sms_from, body_of_sms):
    logger.debug(
        "".join(
            ["User: ", players_database[sms_from][CALLERNAME], " asked for Form-Help."]
        )
    )
    return WEBFORM_HELP


def Send_players_list(msid, sms_from, body_of_sms):
    """Send an SMS to CONTROLLER of ALL registered players."""
    for player in list_players_in_database():
        #  Attach the disclaimer instructions on how to STOP texts
        Send_SMS(
            "".join(
                [
                    players_database[player][CALLERNAME],
                    " with ",
                    str(players_database[player][PLUS_ONES]),
                ]
            ),
            CONTROLLER,
        )
        logger.debug(
            "".join(
                [
                    "Player: ",
                    players_database[player][CALLERNAME],
                    " has ",
                    str(players_database[player][PLUS_ONES]),
                    " extra seats.",
                ]
            )
        )


COMMANDS = {
    "Commands": ReturnCommandList,  # return this list of keys.
    "Webform": Send_Webform_help,  # provide a clickable link to the webform.
    "Common": Send_common_commands_help,  # provide help using most common commands.
    "Minus": RemoveReservation,  # remove a +1 from the caller's table.
    "Table": ReturnTableName,  # return callers table name.
    "Team": SetTeamName,  # return Team name if exists or ask if None.
    "Status": ReturnStatus,  # return caller status info.
    "Plus": AddReservation,  # add another +1 to the caller's table.
    "Funny": SuggestFunny,  # return a random "funny" team name from a list.
    "Serious": SuggestSerious,  # return a "serious" team name.
    "Change-Name": ChangePlayerName,  # delete the player name and ask for a new one.
    "Change-Team": ChangeTeamName,  # delete the team name and ask for a new one.
    "time": ReturnHelpInfo,  # return the HELP file with info on start time of game.
    "Helpme": ReturnHelpInfo,  # return the HELP file with info on using the app.
    "Shuffle": ShuffleTables,  # CONTROLLER ONLY: re-shuffle table assignments.
    "Start": StartGame,  # CONTROLLER ONLY: Lock-in the table assignments for thid game night.
    "Size": ChangeTeamSize,  # CONTROLLER ONLY: Change the number of players per table.
    "Announcement": Send_Announcement,  # CONTROLLER ONLY: Make a SMS note to all registered players.
    "Players-list": Send_players_list,  # CONTROLLER ONLY: Make a SMS note to all registered players.
}
CONTROLLER_ONLY_COMMANDS = [
    "Announcement",
    "Players-list",
    "Shuffle",
    "Start",
    "Size",
]

# Save a dictionary into a pickle file.
import pickle

# pickle.dump( players_database, open( DATABASE_PATHOBJ, "wb" ) )
# retrieve database:
# players_database = pickle.load( open( DATABASE_PATHOBJ, "rb" ) )
if DATABASE_PATHOBJ.exists():
    logger.info("Recovering pickle database...")
    players_database = pickle.load(open(DATABASE_PATHOBJ, "rb"))
else:
    logger.info("Creating new pickle database...")
    pickle.dump(players_database, open(DATABASE_PATHOBJ, "wb"))


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


def Send_SMS(text, receipient):
    # TODO place a block on SMS between 10pm and 8am
    logger.info("".join([text, ":-to-:", receipient]))
    return CLIENT.messages.create(body=text, from_=TWILLIO_SMS_NUMBER, to=receipient)


def Respond_to(msid, sms_from, body_of_sms):
    response = update_caller_database(msid, sms_from, body_of_sms)
    logger.info(pprint_dicts(players_database[sms_from]))
    cmnds = COMMANDS.keys()
    logger.info(cmnds)
    for word in cmnds:
        if word.lower() in str(body_of_sms).lower():
            logger.info("".join(["Found command: ", word]))
            if word in CONTROLLER_ONLY_COMMANDS:
                if sms_from == CONTROLLER:
                    response = COMMANDS[word](msid, sms_from, body_of_sms)
                else:
                    logger.info("Command not available to this user.")
                    response = "Sorry, That command is only available to the controller of this app."
            else:
                response = COMMANDS[word](msid, sms_from, body_of_sms)
        else:
            logger.debug("".join(["Did not find ", word, " in ", str(body_of_sms)]))
    else:
        logger.info("No command words found in this SMS.")
    return response


def update_caller_database(msid, sms_from, body_of_sms):
    response = "The Robots are coming!  LoL  Head for the hills "
    response = "".join([response, players_database[sms_from][CALLERNAME]])
    players_database[sms_from][MESSAGE_HISTORY].append((body_of_sms, msid))
    messages_list = players_database[sms_from][MESSAGE_HISTORY]
    # truncate list at last 5 messages.
    players_database[sms_from][MESSAGE_HISTORY] = messages_list[-5:]
    logger.info("".join(["Caller's Name: ", players_database[sms_from][CALLERNAME]]))
    if players_database[sms_from][FIRSTCALL] == None:
        logger.info("First time caller.")
        Send_SMS("New Caller logged.", CONTROLLER)
        players_database[sms_from][FIRSTCALL] = dt.datetime.now(pytz.timezone("UTC"))
        response = ask_caller_their_name()
        players_database[sms_from][RECENTCALL] = dt.datetime.now(pytz.timezone("UTC"))
    else:
        if players_database[sms_from][CALLERNAME] == "":
            response = check_sms_for_name(msid, sms_from, body_of_sms)
        players_database[sms_from][RECENTCALL] = dt.datetime.now(pytz.timezone("UTC"))
    return response


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


print(Send_SMS("SpeedTrivia program start.", "+18125577095"))

logger.info("Instantiating Flask App:")
SpeedTriviaApp = Flask(__name__)
logger.info(SpeedTriviaApp)


@SpeedTriviaApp.route("/sms", methods=["GET", "POST"])
def sms_reply():
    """Respond to incoming calls.
    This is the entrypoint for SpeedTrivia functionality.
    """
    logger.info("Message received:")
    sms_body = request.values.get("Body", None)
    sms_from = request.values.get("From", None)
    sms_MSID = request.values.get("MessageSid", None)
    logger.info(sms_MSID)
    logger.info(sms_from)
    logger.info(sms_body)
    # Start our TwiML response by creating a new response object.
    sms_response = MessagingResponse()
    logger.info(sms_response)
    # Generate an appropriate response (if any)
    reply = Respond_to(sms_MSID, sms_from, sms_body)
    if reply == "":
        logger.info("No response needed.")
    else:
        logger.info(reply)
    sms_response.message(reply)
    logger.info(str(sms_response))
    logger.info("Updating database...")
    pickle.dump(players_database, open(DATABASE_PATHOBJ, "wb"))
    logger.info("Returning control to Flask.")
    return str(sms_response)


if __name__ == "__main__":
    try:
        logger.info("Program is being run as __main__")
        SpeedTriviaApp.run()
        logger.info("Program ended nominally.")
        sys.exit(0)
    except Exception as e:
        logger.info("Program terminated with exception:")
        logger.info(str(e))
        sys.exit(0)
