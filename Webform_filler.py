"""Take a string of text from SMS and fill out trivia form.
"""

from loguru import logger
from Selenium import Fill_and_submit_trivia_form
from pprint import pformat as pprint_dicts

def Check_for_webform_answer_submission(msid, sms_from, body_of_sms):
    """Take a string in the form: RxQxPxxAany text to the end of the string as an answer.

    Args:
        msid (string): Message ID from Twilio
        sms_from (string): 12 character string of sending phone number.
        body_of_sms (string): Boby of the SMS string

    Returns:
        (string): Text message to be returned to sender by Twilio.
    """
    data = {}
    data['team'] = 'WooHoo!'
    data['submit'] = False
    t = body_of_sms.lower()
    if (t[0] == 'r'):
        # First character matches pattern
        if t[1] == 'f':
            data['round'] = 'Final'
        elif t[1] == 'h':
            data['round'] = 'Halftime'
        elif t[1] == 't':
            data['round'] = 'Tiebreaker'
        else:
            data['round'] = t[1]
        if t[2] == 'q':
            # this matches rounds 1 through 6
            data['question'] = t[3]
            if t[4] == 'p':
                data['points'] = t[5]
                data['answer'] = body_of_sms[7:]      
        elif t[2] == 'a':
            # This pattern matches Halftime.
            Answers = body_of_sms[3:].split('#')
            if len(Answers) < 5:
                # good result
                data['answer'] = Answers
                # TODO end here and send form
            else:
                # trim answers or ask for clarification.
                data['answer'] = Answers
        elif t[2] == 'p':
            # This pattern matches Final round
            Points = t[3]  # there's always at least one digit points wagered
            data['points'] = Points
            Answers = body_of_sms[5:].split('#')
            data['answer'] = Answers
            if t[4] in '0123456789':
                Points = t[3:5]  # this is a 2 digit points wager    
                Answers = body_of_sms[6:].split('#')
                data['answer'] = Answers
                data['points'] = Points
        logger.info(f'SMS decoded as: {pprint_dicts(data)}')
        result = Fill_and_submit_trivia_form(data)
    else:
        logger.info(f'SMS does not match a trivia answer format.')
        result = 'Did not recognize a trivia answer.'  # no response to the sender
    return result
