"""Take a string of text from SMS and fill out trivia form.
"""

from loguru import logger
from Selenium import Fill_and_submit_trivia_form
from pprint import pformat as pprint_dicts
from team import Team

from ST_Twilio import Send_SMS

def Check_for_webform_answer_submission(msid, sms_from, body_of_sms, teamname, Send=False):
    """Take a string in the form: RxQxPxxAany text to the end of the string as an answer.

    Args:
        msid (string): Message ID from Twilio
        sms_from (string): 12 character string of sending phone number.
        body_of_sms (string): Boby of the SMS string

    Returns:
        (string): Text message to be returned to sender by Twilio.
    """
    answer_fmt = determine_answer_format(body_of_sms)
    if answer_fmt == "precise":
        data = parse_precise_answer(teamname, body_of_sms, Send)
        logger.info(f"SMS decoded as:\n{pprint_dicts(data)}")
        Send_SMS(f'{pprint_dicts(data)}', sms_from)        
        result = Fill_and_submit_trivia_form(data, Send=data['submit'])

    elif answer_fmt == "tracked":
        team = Team.get_team_by_name(teamname)
        parsed_answer = parse_tracked_answer(team, body_of_sms, Send)
        logger.info(f"SMS decoded as:\n{pprint_dicts(parsed_answer)}")
        Send_SMS(f'{pprint_dicts(parsed_answer)}', sms_from)        
        result = Fill_and_submit_trivia_form(parsed_answer, Send=parsed_answer['submit'])
    else:
        logger.info(f"SMS does not match a trivia answer format.")
        result = "Did not recognize a trivia answer."  # no response to the sender
    return result

def determine_answer_format(sms_body:str) -> str:
    """
    Scan an SMS body to determine which format the answer is in (and therefore which parsing function to use)

    Parameters:
        sms_body (str): The raw SMS body

    Returns:
        format (str): A word describing the format. (eg. "precise", "tracked")
    """
    first_char = sms_body[0].upper()
    if first_char == "R":
        return "precise"
    elif first_char.isdigit():
        return "tracked"
    else:
        return "unrecognized"

def parse_precise_answer(teamname: str, body_of_sms: str, Send: bool=False) -> dict:
    result = 'Undefined webform submission error.'
    data = {}
    data["team"] = teamname
    data["submit"] = Send
    t = body_of_sms.lower()
    # First character matches pattern
    if t[1] == "f":
        data["round"] = "Final"
    elif t[1] == "h":
        data["round"] = "Halftime"
    elif t[1] == "t":
        data["round"] = "Tiebreaker"
    else:
        data["round"] = t[1]
    if t[2] == "q":
        # this matches rounds 1 through 6
        data["question"] = t[3]
        if t[4] == "p":
            data["points"] = t[5]
            data["answer"] = body_of_sms[7:]
    elif t[2] == "a":
        # This pattern matches Halftime.
        Answers = body_of_sms[3:].split("#")
        if len(Answers) < 5:
            # good result
            data["answer"] = Answers
            # TODO end here and send form
        else:
            # trim answers or ask for clarification.
            data["answer"] = Answers
    elif t[2] == "p":
        # This pattern matches Final round
        Points = t[3]  # there's always at least one digit points wagered
        data["points"] = Points
        Answers = body_of_sms[5:].split("#")
        data["answer"] = Answers
        if t[4] in "0123456789":
            Points = t[3:5]  # this is a 2 digit points wager
            Answers = body_of_sms[6:].split("#")
            data["answer"] = Answers
            data["points"] = Points
    return data

def parse_tracked_answer(team: Team, sms_body: str, send: bool=False) -> dict:
    """
    Parses a simplified SMS message into the data dict needed by Fill_and_submit_trivia_form.
    Requires that the Team object is set up and tracking rounds/questions
    
    Parameters:
        team (Team): The Team object of the submitter
        sms_body (str): Received SMS message body. Calling function will have confirmed the first word is points
        send (bool): Whether or not to actually submit

    Returns:
        data (dict): A data dict ready to submit
    """
    data = {
        "team": team.name,
        "question": str(team.question),
        "round": str(team.round),
        "submit": send,
    }

    parts = sms_body.split(' ')
    points = parts[0]

    try:
        int(points)
    except ValueError:
        error = f"Points not a valid number ({points})"
    
    answer = ' '.join(parts[1:]) # recombine the other parts

    data["points"] = points
    data["answer"] = answer

    return data