import random
import time
import datetime as dt
import sys
from pprint import pformat as pprint_dicts

import pytz
from flask import Flask, redirect, request
from loguru import logger

from ST_common import *
from ST_Twilio import Send_SMS
from Webform_filler import Check_for_webform_answer_submission

UNKNOWN_CALLER = 0
NAMED_CALLER = 234
NEW_CALLER = 123

@logger.catch
def Respond_to(msid, sms_from, body_of_sms):
    """Takes incoming SMS details and determines correct response.

    Args:
        msid (str)): Twilio message ID
        sms_from (str): 12 character phone number
        body_of_sms (str): Actual text of incoming SMS

    Returns:
        str: The string sent back to the caller.
    """
    response, caller_type = update_caller_database(msid, sms_from, body_of_sms)
    logger.info(pprint_dicts(players_database[sms_from]))
    if caller_type == NEW_CALLER:
        return response
    if caller_type == NAMED_CALLER: # new player name has been found and entered.
        return response
    cmnds = COMMANDS.keys()
    # logger.info(cmnds)
    for word in cmnds:
        command_slice = str(body_of_sms).lower()[: len(word)]
        # logger.debug(f'SMS slice from front of text: {command_slice}')
        if word.lower() == command_slice:
            # ALTERNATE APPROACH: Ensure that only whole words are matched.
            # search = word.lower()
            # strn = str(body_of_sms).lower()
            # matches = re.findall(r"\b" + search + r"\b", strn)
            # matches is a list of each match.
            logger.info(f"Found command: {word}")
            # slice off command from front of string
            action_value = body_of_sms[len(word) :]
            logger.debug(f"Command action value is: {action_value}")
            logger.debug(f"Attempting to call function: {COMMANDS[word]}")
            if word in CONTROLLER_ONLY_COMMANDS:
                if sms_from == CONTROLLER:
                    response = COMMANDS[word](msid, sms_from, action_value)
                else:
                    logger.info("Command not available to this user.")
                    response = "Sorry, That command is only available to the CONTROLLER of this app."
            else:
                response = COMMANDS[word](msid, sms_from, action_value)
            # break loop here to stop after first command word found.
            break
        else:
            pass
            # logger.debug(f"Did not find '{word}' in '{body_of_sms}'")
    else:
        logger.info("No command words found in this SMS.")
        logger.debug(f"Checking for a trivia answer form in SMS...")
        if TESTING:
            response = "System under test."
            print(
                Check_for_webform_answer_submission(
                    msid,
                    sms_from,
                    body_of_sms,
                    players_database[sms_from][CURRENT_TEAM_NAME],
                    Send=False,
                )
            )
        else:
            # TODO Ensure that the function below does not fail silently due to bad data in body_of_sms
            response = Check_for_webform_answer_submission(
                msid,
                sms_from,
                body_of_sms,
                players_database[sms_from][CURRENT_TEAM_NAME],
                Send=True,
            )
    return response


@logger.catch
def update_caller_database(msid, sms_from, body_of_sms):
    caller_type = UNKNOWN_CALLER
    response = f"The Robots are coming!  LoL  Head for the hills {players_database[sms_from][CALLERNAME]}"
    players_database[sms_from][MESSAGE_HISTORY].append((body_of_sms, msid))
    messages_list = players_database[sms_from][MESSAGE_HISTORY]
    # truncate list at last 5 messages.
    players_database[sms_from][MESSAGE_HISTORY] = messages_list[-5:]
    logger.info(f"Caller's Name: {players_database[sms_from][CALLERNAME]}")
    if players_database[sms_from][FIRSTCALL] == None:
        players_database[sms_from][FIRSTCALL] = dt.datetime.now(pytz.timezone("UTC"))
        caller_type, response = ask_caller_their_name()
    else:
        if players_database[sms_from][CALLERNAME] == "":
            response = check_sms_for_name(msid, sms_from, body_of_sms)
    players_database[sms_from][RECENTCALL] = dt.datetime.now(pytz.timezone("UTC"))
    return caller_type, response


@logger.catch
def ask_caller_their_name():
    logger.info("First time caller.")
    Send_SMS("New Caller logged.", CONTROLLER) # send a status update to the primary user
    logger.info("Asking the caller their name.")
    return UNKNOWN_CALLER, "Hello! I don't have your number in my records. Could you please tell me your name?"


@logger.catch
def check_sms_for_name(msid, sms_from, body_of_sms):
    # Function to extract the proper names from free form text.
    logger.info("Searching the sms for the callers name.")
    if (body_of_sms == None) or (len(body_of_sms) <= 0):
        return "Empty Message"
    callername = ProperNounExtractor(body_of_sms)
    if callername == "Changename":
        callername = body_of_sms.split()[1]  # Kludge
    if callername != None:
        logger.info("Found a name:")
        logger.info(callername)
        Send_SMS(f"New Caller is: {callername}", CONTROLLER)
        players_database[sms_from][CALLERNAME] = callername
    else:
        logger.info("Couldn't find a name.")
        return "Sorry. I didn't understand.  Please try again. Feel free to speak in full sentences."
    return f"Thanks {callername}! Glad to meet you. Welcome to SpeedTrivia."


@logger.catch
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


@logger.catch
def how_long_ago_is(past_time):
    delta_ = dt.datetime.now(pytz.timezone("UTC")) - past_time
    days_ = delta_ / dt.timedelta(days=1)
    logger.debug(f"Time since last contact: {days_:.2f} days.")
    return days_


@logger.catch
def AddReservation(msid, sms_from, body_of_sms):
    """Add a +1 to this players table."""
    logger.info("Add a plue one function entered.")
    items = body_of_sms.split()
    try:
        number = int(items[1])
    except (ValueError, IndexError) as e:
        number = 1
    players_database[sms_from][PLUS_ONES] += number
    return f"You now have {players_database[sms_from][PLUS_ONES] + 1} reserved seats at your table counting yourself."


@logger.catch
def RemoveReservation(msid, sms_from, body_of_sms):
    """Players can reserve extra seats at their table for special guests.
    Those guests don't register with this app on their own they just sit
    at the same table by design. (e.g. a non-player or spouse.)
    """
    logger.info("Remove a plus one from player function entered.")
    items = body_of_sms.split()
    try:
        number = int(items[1])
    except (ValueError, IndexError) as e:
        number = 1
    if (players_database[sms_from][PLUS_ONES] - number) >= 0:
        players_database[sms_from][PLUS_ONES] -= number
    else:
        players_database[sms_from][PLUS_ONES] = 0
    return f"You now have {players_database[sms_from][PLUS_ONES] + 1} reserved seats at your table counting yourself."


@logger.catch
def ReturnTableName(msid, sms_from, body_of_sms):
    """Table name is an index value. (e.g. Gamma, delta, epsilon...)"""
    logger.info("return player team table label function entered.")
    return f"Your table is {players_database[sms_from][CURRENT_TABLE_ASSIGNMENT]}."


@logger.catch
def SetTeamName(msid, sms_from, body_of_sms):
    """Team name is the formal name. (e.g. 'Fools for the Trivia')
    When entered for one player applies for all at table.
    """
    logger.info("Set team name function entered.")
    teamname = body_of_sms
    players_database[sms_from][CURRENT_TEAM_NAME] = teamname
    return f"Your new team name is: {teamname}"


@logger.catch
def list_players_in_database(tonight=False):
    tp_list = []
    for k in players_database.keys():
        if (
            (k != None) and (len(k) == 12) and (k[0] == "+")
        ):  # ignore entries that are not phone numbers
            # Entries that are not phone numbers are system variables for internal use.
            # TODO this could be made more robust with a regex ('+1dddddddddd')
            dlta = how_long_ago_is(players_database[k][RECENTCALL])
            if tonight:  # Filter out records from past weeks if tonight equal True.
                if dlta < 6:
                    tp_list.append(k)
            else:
                tp_list.append(k)
    return tp_list


@logger.catch
def Tonights_players():
    return list_players_in_database(tonight=True)


@logger.catch
def ReturnStatus(msid, sms_from, body_of_sms):
    """Return various details of this player."""
    logger.info("Send status to player function entered.")
    stat = f"{players_database[sms_from][CALLERNAME]} your team name is {players_database[sms_from][CURRENT_TEAM_NAME]} and your table name is {players_database[sms_from][CURRENT_TABLE_ASSIGNMENT]} and you have {players_database[sms_from][PLUS_ONES]} extra seats reserved."
    if sms_from == CONTROLLER:
        stat = f"{stat} --status: {TABLESIZE} per table. {len(Tonights_players())} players registered for tonight."
    return stat


@logger.catch
def SuggestFunny(msid, sms_from, body_of_sms):
    """Return some ideas for team names."""
    logger.info("Funny team name suggestions function entered.")
    result = ""
    while len(result) < 140:
        result = result + random.choice(POSSIBLE_TEAM_NAMES)
    return result


@logger.catch
def SuggestSerious(msid, sms_from, body_of_sms):
    """Suggest only serious names."""
    logger.info("Serious team name suggestions function entered.")
    return msid


@logger.catch
def ChangePlayerName(msid, sms_from, value_slice):
    """Allow player to correct their own name."""
    logger.info("Change players name function entered.")
    if value_slice != None:
        players_database[sms_from][CALLERNAME] = value_slice
        reply = f"Thanks {value_slice}! Your name has been updated."
    else:
        reply = "Sorry, I did not understand."
    return reply


@logger.catch
def ReturnHelpInfo(msid, sms_from, body_of_sms):
    """Returns basic info about this app and the trivia competition."""
    logger.info("Help info function entered.")
    return HELPFUL_INFO


@logger.catch
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
        logger.debug(f"{plus_ones} Extra players")
        return plus_ones

    def open_chairs(table):
        open_chrs = TABLESIZE - (len(table) + extra_players(table))
        logger.debug(f"{open_chrs} Open chairs.")
        if open_chrs < 1:
            return 0
        return open_chrs

    def Assign_Tables(tables, players):
        tbl_dict = defaultdict(list)
        for player in players:
            while player != None:
                rnd_table = random.choice(tables)
                logger.debug(f"{rnd_table} random table.")
                if open_chairs(tbl_dict[rnd_table]) > 0:
                    tbl_dict[rnd_table].append(player)
                    logger.debug(f"{player} assigned to table.")
                    player = None
        return tbl_dict

    # Begin ShuffleTables:
    logger.info("Shuffle tables function entered.")
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
    logger.debug(f"{TONIGHTS_PLAYERS} Tonights players.")
    TOT_PLAYERS = len(TONIGHTS_PLAYERS) + extra_players(TONIGHTS_PLAYERS)
    logger.debug(f"{TOT_PLAYERS} Total players.")
    NUM_OF_TABLES = int(TOT_PLAYERS / TABLESIZE) + 1
    if NUM_OF_TABLES < 1:
        NUM_OF_TABLES = 1
    tables = TABLE_NAMES[:NUM_OF_TABLES]
    logger.debug(f"{tables} Tonights tables.")

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
            logger.debug(f"Table collisions: {table_collisions}")
        logger.debug(f"Player collisions: {Total_collisions}")
        return Total_collisions

    NUMBER_OF_GUESSES = len(TONIGHTS_PLAYERS)
    guesses = dict()
    for itr in range(NUMBER_OF_GUESSES):
        guesses[itr] = Proposed_assignments()
        logger.debug(f"Guess {itr} is {pprint_dicts(guesses[itr])}")
    least_meetups = dict()
    meets = 80000
    for guess in guesses.keys():
        logger.debug(f"Calculating past meetups for proposal: {guess}")
        tnom = Total_number_of_meetups(guesses[guess])
        if meets > tnom:
            meets = tnom
            least_meetups = guesses[guess]
    logger.debug(f"Most unique tables are: {pprint_dicts(least_meetups)}")
    for table in least_meetups.keys():
        logger.debug(f"processing table {table}")
        for player in least_meetups[table]:
            logger.debug(f"     processing player {player}")
            TABLE_ASSIGNED[player] = table
    # final number of tables may be less than original estimation so re-establish
    tables = least_meetups.keys()
    logger.info(f"Tonights tables are: {tables}")
    return "Players have been assigned tables."


@logger.catch
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
        sms_text = f"SpeedTrivia suggests you sit at table: {TABLE_ASSIGNED[player]}"
        if TESTING == True:
            logger.info(f'Update: "{sms_text}" NOT SENT to {player}.')
        else:
            Send_SMS(sms_text, player)
            logger.info(f'"{sms_text}" sent to {player}')
        time.sleep(0.02)  # for delay between SMS messages (probably not needed)
        # add other players from table to history list
        for teammate in least_meetups[TABLE_ASSIGNED[player]]:
            if teammate == player:
                pass
            else:
                logger.debug(f"Adding : {teammate} to {player}")
                players_database[player][PARTNER_HISTORY].append(teammate)
                # TODO consider if this should be a database with teammates and dates.
                # for now it just a list with duplicates.
    return "Players have been notified."


@logger.catch
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
    return f"New table size = {TABLESIZE}"


@logger.catch
def Send_Announcement(msid, sms_from, body_of_sms):
    """Send an SMS to ALL registered players."""
    logger.info("Entering bulk announcement function")
    announcement = body_of_sms
    for player in list_players_in_database():
        #  Attach the disclaimer instructions on how to STOP texts
        if TESTING == True:
            logger.info(f'Announcement: "{announcement}" NOT SENT to {player}.')
        else:
            Send_SMS(announcement, player)
            logger.info(f'Announcement: "{announcement}" sent to {player}')
    logger.info("Bulk announcement sent.")
    return "Bulk announcement sent."


@logger.catch
def Send_common_commands_help(msid, sms_from, body_of_sms):
    logger.debug(f"User: {players_database[sms_from][CALLERNAME]} asked for Form-Help.")
    return MOST_COMMON_HELP


@logger.catch
def Send_Webform_help(msid, sms_from, body_of_sms):
    logger.debug(f"User: {players_database[sms_from][CALLERNAME]} asked for Form-Help.")
    return WEBFORM_HELP


@logger.catch
def Send_players_list(msid, sms_from, body_of_sms):
    """Send an SMS to CONTROLLER of ALL registered players."""
    player_list = []
    for player in list_players_in_database():
        player_list.append(
            f"{players_database[player][CALLERNAME]} with {players_database[player][PLUS_ONES]} extras. "
        )
    # this .join is the best approach to combine all the strings in the list.
    message = "".join(player_list)
    logger.debug(message)
    return message
