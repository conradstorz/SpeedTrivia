import sys
from time import sleep
from selenium import webdriver
from loguru import logger
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pprint import pformat as pprint_dicts

SENDFORM = True
TeamNameBoxID = "input_14"
GameRoundBoxID = "input_17"
GameQuestionBoxID = "input_18"
FirstHalfPointBoxID = "input_16"
SecondHalfPointBoxID = "input_19"
AnswerBoxID = "input_6"
SubmitButtonID = "input_7"
HalftimeAndFinalAnswerBoxIDs = [
    "input_20",
    "input_21",
    "input_22",
    "input_23",
]
FinalQuestionWagerID = "input_24"


def Fill_a_field(webobj, value, field_id):
    logger.debug("fill field")
    logger.debug(f"field: {field_id} Value: {value}")
    sleep(0.1)
    field = webobj.find_element_by_id(field_id)
    field.send_keys(value)
    return


def Fill_a_dropdown(webobj, value, field_id):
    logger.debug("fill dropdown")
    logger.debug(f"field: {field_id} Value: {value}")
    sleep(0.1)
    dropdn = Select(webobj.find_element_by_id(field_id))
    dropdn.select_by_value(value)
    return


def Fill_four_answers(webobj, values, field_ids):
    """This requires multiple values and fields in lists"""
    logger.debug("fill 4 answers")
    logger.debug(f"field: {field_ids} Value: {values}")
    for indx, field in enumerate(field_ids):
        Fill_a_field(webobj, values[indx], field)
    return


def Click_a_button(webobj, value, field_id):
    sleep(0.1)
    logger.debug("click option")
    logger.debug(f"field: {field_id} Value: {value}")
    button = webobj.find_element_by_id(field_id)
    if value == True:
        button.click()
    else:
        logger.debug("Submit button not pressed by request.")
    return


def Pass_(value, field_id):
    logger.debug("pass option")
    logger.debug(f"field: {field_id} Value: {value}")
    pass


WEBFORM = {
    "1": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field, 'valid_response': 'any'},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown, 'valid_response': ['1','2','3','Halftime','4','5','6','Final','Tiebreaker']},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown, 'valid_response': ['1', '2', '3']},
        "points": {"fld": FirstHalfPointBoxID, "func": Fill_a_dropdown, 'valid_response': ['2','4','6']},
        "answer": {"fld": AnswerBoxID, "func": Fill_a_field, 'valid_response': 'any'},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button, 'valid_response': [True,False]},
    },
    "2": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field, 'valid_response': 'any'},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown, 'valid_response': ['1','2','3','Halftime','4','5','6','Final','Tiebreaker']},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown, 'valid_response': ['1', '2', '3']},
        "points": {"fld": FirstHalfPointBoxID, "func": Fill_a_dropdown, 'valid_response': ['2','4','6']},
        "answer": {"fld": AnswerBoxID, "func": Fill_a_field, 'valid_response': 'any'},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button, 'valid_response': [True,False]},
    },
    "3": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field, 'valid_response': 'any'},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown, 'valid_response': ['1','2','3','Halftime','4','5','6','Final','Tiebreaker']},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown, 'valid_response': ['1', '2', '3']},
        "points": {"fld": FirstHalfPointBoxID, "func": Fill_a_dropdown, 'valid_response': ['2','4','6']},
        "answer": {"fld": AnswerBoxID, "func": Fill_a_field, 'valid_response': 'any'},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button, 'valid_response': [True,False]},
    },
    "Halftime": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field, 'valid_response': 'any'},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown, 'valid_response': ['1','2','3','Halftime','4','5','6','Final','Tiebreaker']},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown, 'valid_response': []},
        "points": {"fld": FirstHalfPointBoxID, "func": Fill_a_dropdown, 'valid_response': []},
        "answer": {"fld": HalftimeAndFinalAnswerBoxIDs, "func": Fill_four_answers, 'valid_response': 'any'},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button, 'valid_response': [True,False]},
    },
    "4": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field, 'valid_response': 'any'},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown, 'valid_response': ['1','2','3','Halftime','4','5','6','Final','Tiebreaker']},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown, 'valid_response': ['1', '2', '3']},
        "points": {"fld": SecondHalfPointBoxID, "func": Fill_a_dropdown, 'valid_response': ['5','7','9']},
        "answer": {"fld": AnswerBoxID, "func": Fill_a_field, 'valid_response': 'any'},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button, 'valid_response': [True,False]},
    },
    "5": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field, 'valid_response': 'any'},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown, 'valid_response': ['1','2','3','Halftime','4','5','6','Final','Tiebreaker']},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown, 'valid_response': ['1', '2', '3']},
        "points": {"fld": SecondHalfPointBoxID, "func": Fill_a_dropdown, 'valid_response': ['5','7','9']},
        "answer": {"fld": AnswerBoxID, "func": Fill_a_field, 'valid_response': 'any'},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button, 'valid_response': [True,False]},
    },
    "6": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field, 'valid_response': 'any'},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown, 'valid_response': ['1','2','3','Halftime','4','5','6','Final','Tiebreaker']},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown, 'valid_response': ['1', '2', '3']},
        "points": {"fld": SecondHalfPointBoxID, "func": Fill_a_dropdown, 'valid_response': ['5','7','9']},
        "answer": {"fld": AnswerBoxID, "func": Fill_a_field, 'valid_response': 'any'},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button, 'valid_response': [True,False]},
    },
    "Final": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field, 'valid_response': 'any'},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown, 'valid_response': ['1','2','3','Halftime','4','5','6','Final','Tiebreaker']},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown, 'valid_response': []},
        "points": {"fld": FinalQuestionWagerID, "func": Fill_a_field, 'valid_response': ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']},
        "answer": {"fld": HalftimeAndFinalAnswerBoxIDs, "func": Fill_four_answers, 'valid_response': 'any'},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button, 'valid_response': [True,False]},
    },
    "Tiebreaker": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field, 'valid_response': 'any'},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown, 'valid_response': ['1','2','3','Halftime','4','5','6','Final','Tiebreaker']},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown, 'valid_response': []},
        "points": {"fld": FirstHalfPointBoxID, "func": Fill_a_dropdown, 'valid_response': []},
        "answer": {"fld": AnswerBoxID, "func": Fill_a_field, 'valid_response': 'any'},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button, 'valid_response': [True,False]},
    },
}

sample_answers = {
    "1": {
        "team": "FirstRound",
        "round": "1",
        "question": "2",
        "points": "6",
        "answer": "First round answer",
        "submit": SENDFORM,
    },
    "halftime": {
        "team": "Halftime Round",
        "round": "Halftime",
        "answer": [
            "alpha",
            "beta",
            "delta",
            "gamma",
        ],
        "submit": SENDFORM,
    },
    "4": {
        "team": "Second Round",
        "round": "4",
        "question": "2",
        "points": "9",
        "answer": "second round answer",
        "submit": SENDFORM,
    },
    "final": {
        "team": "Final Questions",
        "round": "Final",
        "answer": [
            "alpha",
            "beta",
            "delta",
            "gamma",
        ],
        "points": "20",
        "submit": SENDFORM,
    },
    "tiebreaker": {
        "team": "Tiebreaker round",
        "round": "Tiebreaker",
        "answer": "The final decision (no points)",
        "submit": SENDFORM,
    },
}


def Fill_and_submit_trivia_form(data, Send=False):
    """Launch a browser and fill fields of webform then submit.
    The format of the 'data' variable varies based on the form to be filled.
    Round 1 and Round 2 forms are identical differing only in the 'field labels' in use.
    Halftime and FinalRound are the same but use 4 answer boxes. These rounds require
    the 'answer' and 'field' variable to be a list of 4 items each corresponding to
    the box 'field label' and 'answer text' for each of the four answers.
    Tiebrasker round is different in that it only has an answer and no points field.
    Example data dictionary:
    {   "team": "My Team Name",
        "round": "1",  # values are 1-6, Halftime, Final, Tiebreaker
        "question": "2",  # values are 1-3
        "points": "6",  # firstround is 2,4,6  secondround is 5,7,9
        "answer": "Place your answer here",
        "submit": True,}  # use False for testing.
    """
    browser_token = webdriver.Chrome()
    browser_token.get("https://form.jotform.com/202575177230149")
    fields_and_functions = WEBFORM[data["round"]]
    logger.debug(fields_and_functions)
    logger.debug("...")
    logger.debug(data)
    # fill the 'Round' value on the form first.
    Round = data.pop("round")
    Submit = data.pop('submit')
    legal_values = fields_and_functions['round']['valid_response']
    if Round in legal_values:
        logger.debug('Ready to set the round field of form.')
        fields_and_functions["round"]["func"](
            browser_token, Round, fields_and_functions["round"]["fld"]
        )
        logger.debug('Round set.')
    else:
        logger.error(f'Round: {Round} not found in {legal_values}')
        return f'Acceptable Round values are {legal_values}'
    # form is now initialized to accept the correct data
    valid_fields = fields_and_functions.keys()
    for field, value in data.items():
        if field in valid_fields:        
            legal_values = fields_and_functions[field]['valid_response']
            # TODO validate that the value is acceptable for the field it is being offered.
            # if value_is_acceptable(value, legal_values):
            # proceede
            # else log error
            logger.debug(f"Field: {field} Value: {value} Acceptable responses: {legal_values}")
            fields_and_functions[field]["func"](
                browser_token, value, fields_and_functions[field]["fld"]
            )
            # TODO error check the browser form
            logger.debug('Field filled.')
        else:
            logger.error(f'Field: {field} not found in: {valid_fields}')
            return f'Input Field: {field} not found in {valid_fields}'
    # Now submit the form if True
    logger.debug('Ready to submit form.')
    legal_values = fields_and_functions['submit']['valid_response']
    if Submit in legal_values:
        fields_and_functions["submit"]["func"](
            browser_token, Submit, fields_and_functions["submit"]["fld"]
        )
    else:
        logger.error(f'Submit failed. Value: {Submit} not in {legal_values}')
        return 'Submit of form failed.'
    sleep(.5)
    browser_token.close()
    data['submit'] = Submit  # place submit field back into dictionary
    data['round'] = Round  # place round entry back into dictionary
    return f"Trivia form sent:\n{pprint_dicts(data)}"


@logger.catch
def main():
    for k, sampleform in sample_answers.items():
        Fill_and_submit_trivia_form(sample_answers[k], Send=False)
    sleep(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
