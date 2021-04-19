"""Take a string of text from SMS and fill out trivia form.
"""

from loguru import logger
from Seleniumtest import Fill_and_submit_trivia_form

def Check_for_webform_answer_submission(msid, sms_from, body_of_sms):
    """Take a string in the form: RxQxPxxAany text to the end of the string as an answer.

    Args:
        msid (string): Message ID from Twilio
        sms_from (string): 12 character string of sending phone number.
        body_of_sms (string): Boby of the SMS string

    Returns:
        (string): Text message to be returned to sender by Twilio.
    """
    t = body_of_sms.lower()
    if (t[0] == 'r') and (t[2] == 'q') and (t[4] == 'p'):
        # SMS matches format of a trivia answer key.
        Round = t[1]
        Question = t[3]
        Points = t[5]
        if t[6] in ['0123456789']:
            Points = t[5:7]
            Answer = t[7:]
        else:
            Answer = t[6:]
        data = {
            'team': 'Got it!',
            'round': Round,
            'question': Question,
            'points': Points,
            'answer': Answer,
            'submit': False,
        }
        result = Fill_and_submit_trivia_form(data)
    else:
        logger.info(f'SMS does not match a trivia answer format.')
        result = ''  # no response to the sender
    return result
