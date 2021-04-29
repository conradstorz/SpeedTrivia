import sys
from time import sleep
from selenium import webdriver
from loguru import logger
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pprint import pformat as pprint_dicts

THE_JOTFORM_URL = "https://form.jotform.com/202575177230149"
SENDFORM = False  # Control the behaviour of the sample values during testing.
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

WEBFORM_SUBMIT_BUTTON_VALUES = [True, False]
QUESTION_PER_ROUND_VALUES = ['1', '2', '3']
QUESTION_NUMBER_HALFTIME_FINAL_TIEBREAKER = []  # Not required and no field is available
VALID_ROUND_1_POINTS = ['2', '4', '6']
VALID_HALFTIME_POINTS = []  # Not required and no field is available
VALID_ROUND_2_POINTS = ['5', '7', '9']
VALID_FINAL_ROUND_POINTS = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
VALID_TIEBREAKER_POINTS = []  # Not required and no field is available 

FORM_FIELD_ID = "field_id"
PROPER_FUNCTION = "function_pointer"
VALID_RESPONSES = "valid_response"
ROUND = "round"
SUBMIT = "submit"
TEAM_NAME_FIELD = "team"

ROUND_1 = "1"
ROUND_2 = "2"
ROUND_3 = "3"
ROUND_HALFTIME = "Halftime"
ROUND_4 = "4"
ROUND_5 = "5"
ROUND_6 = "6"
ROUND_FINAL = "Final"
ROUND_TIEBREAKER = "Tiebreaker"

FLEXABLE_FIELD_INPUT = "any"  # Flag to indicate any reasonable text can be input.
QUESTION = "question"
POINTS = "points"
ANSWER = "answer"

def Fill_a_field(webobj, value, field_id):
    logger.debug("fill field")
    logger.debug(f"field: {field_id} Value: {value}")
    try:
        field = webobj.find_element_by_id(field_id)
        field.send_keys(value)
        logger.debug("Found and entered value success.")
    except NoSuchElementException as e:
        logger.error(f"Didn't find {value} in {field_id}")
        logger.error(f"{e}")
    return


def Fill_a_dropdown(webobj, value, field_id):
    logger.debug("fill dropdown")
    logger.debug(f"field: {field_id} Value: {value}")
    try:
        dropdn = Select(webobj.find_element_by_id(field_id))
        dropdn.select_by_value(value)
        logger.debug("Found and entered value success.")
    except NoSuchElementException as e:
        logger.error(f"Didn't find {value} in {field_id}")
        logger.error(f"{e}")
    return


def Fill_four_answers(webobj, values, field_ids):
    """This requires multiple values and fields in lists"""
    logger.debug("fill 4 answers")
    logger.debug(f"field: {field_ids} Value: {values}")
    for indx, field in enumerate(field_ids):
        Fill_a_field(webobj, values[indx], field)
    return


def Click_a_button(webobj, value, field_id):
    logger.debug("click option")
    logger.debug(f"field: {field_id} Value: {value}")
    try:
        button = webobj.find_element_by_id(field_id)
        if value == True:
            button.click()
            logger.debug("Found and clicked button success.")
        else:
            logger.debug("Submit button not pressed by request.")
    except NoSuchElementException as e:
        logger.error(f"Didn't find {value} in {field_id}")
        logger.error(f"{e}")
    return


def Pass_(value, field_id):
    logger.debug("pass option")
    logger.debug(f"field: {field_id} Value: {value}")
    pass

WEBFORM = {
    ROUND_1: {
        TEAM_NAME_FIELD: {FORM_FIELD_ID: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FORM_FIELD_ID: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_1,
        },
        QUESTION: {
            FORM_FIELD_ID: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: QUESTION_PER_ROUND_VALUES,
        },
        POINTS: {
            FORM_FIELD_ID: FirstHalfPointBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: VALID_ROUND_1_POINTS,
        },
        ANSWER: {FORM_FIELD_ID: AnswerBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        SUBMIT: {
            FORM_FIELD_ID: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: WEBFORM_SUBMIT_BUTTON_VALUES,
        },
    },
    ROUND_2: {
        TEAM_NAME_FIELD: {FORM_FIELD_ID: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FORM_FIELD_ID: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_2,
        },
        QUESTION: {
            FORM_FIELD_ID: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: QUESTION_PER_ROUND_VALUES,
        },
        POINTS: {
            FORM_FIELD_ID: FirstHalfPointBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: VALID_ROUND_1_POINTS,
        },
        ANSWER: {FORM_FIELD_ID: AnswerBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        SUBMIT: {
            FORM_FIELD_ID: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: WEBFORM_SUBMIT_BUTTON_VALUES,
        },
    },
    ROUND_3: {
        TEAM_NAME_FIELD: {FORM_FIELD_ID: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FORM_FIELD_ID: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_3,
        },
        QUESTION: {
            FORM_FIELD_ID: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: QUESTION_PER_ROUND_VALUES,
        },
        POINTS: {
            FORM_FIELD_ID: FirstHalfPointBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: VALID_ROUND_1_POINTS,
        },
        ANSWER: {FORM_FIELD_ID: AnswerBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        SUBMIT: {
            FORM_FIELD_ID: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: WEBFORM_SUBMIT_BUTTON_VALUES,
        },
    },
    ROUND_HALFTIME: {
        TEAM_NAME_FIELD: {FORM_FIELD_ID: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FORM_FIELD_ID: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_HALFTIME,
        },
        QUESTION: {
            FORM_FIELD_ID: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: QUESTION_NUMBER_HALFTIME_FINAL_TIEBREAKER,
        },
        POINTS: {
            FORM_FIELD_ID: FirstHalfPointBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: VALID_HALFTIME_POINTS,
        },
        ANSWER: {
            FORM_FIELD_ID: HalftimeAndFinalAnswerBoxIDs,
            PROPER_FUNCTION: Fill_four_answers,
            VALID_RESPONSES: FLEXABLE_FIELD_INPUT,
        },
        SUBMIT: {
            FORM_FIELD_ID: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: WEBFORM_SUBMIT_BUTTON_VALUES,
        },
    },
    ROUND_4: {
        TEAM_NAME_FIELD: {FORM_FIELD_ID: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FORM_FIELD_ID: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_4,
        },
        QUESTION: {
            FORM_FIELD_ID: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: QUESTION_PER_ROUND_VALUES,
        },
        POINTS: {
            FORM_FIELD_ID: SecondHalfPointBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: VALID_ROUND_2_POINTS,
        },
        ANSWER: {FORM_FIELD_ID: AnswerBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        SUBMIT: {
            FORM_FIELD_ID: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: WEBFORM_SUBMIT_BUTTON_VALUES,
        },
    },
    ROUND_5: {
        TEAM_NAME_FIELD: {FORM_FIELD_ID: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FORM_FIELD_ID: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_5,
        },
        QUESTION: {
            FORM_FIELD_ID: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: QUESTION_PER_ROUND_VALUES,
        },
        POINTS: {
            FORM_FIELD_ID: SecondHalfPointBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: VALID_ROUND_2_POINTS,
        },
        ANSWER: {FORM_FIELD_ID: AnswerBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        SUBMIT: {
            FORM_FIELD_ID: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: WEBFORM_SUBMIT_BUTTON_VALUES,
        },
    },
    ROUND_6: {
        TEAM_NAME_FIELD: {FORM_FIELD_ID: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FORM_FIELD_ID: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_6,
        },
        QUESTION: {
            FORM_FIELD_ID: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: QUESTION_PER_ROUND_VALUES,
        },
        POINTS: {
            FORM_FIELD_ID: SecondHalfPointBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: VALID_ROUND_2_POINTS,
        },
        ANSWER: {FORM_FIELD_ID: AnswerBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        SUBMIT: {
            FORM_FIELD_ID: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: WEBFORM_SUBMIT_BUTTON_VALUES,
        },
    },
    ROUND_FINAL: {
        TEAM_NAME_FIELD: {FORM_FIELD_ID: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FORM_FIELD_ID: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_FINAL,
        },
        QUESTION: {
            FORM_FIELD_ID: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: QUESTION_NUMBER_HALFTIME_FINAL_TIEBREAKER,
        },
        POINTS: {
            FORM_FIELD_ID: FinalQuestionWagerID,  # NOTE: This field on JotForm is not set "Required" but should be.
            PROPER_FUNCTION: Fill_a_field,
            VALID_RESPONSES: VALID_FINAL_ROUND_POINTS,
        },
        ANSWER: {
            FORM_FIELD_ID: HalftimeAndFinalAnswerBoxIDs,
            PROPER_FUNCTION: Fill_four_answers,
            VALID_RESPONSES: FLEXABLE_FIELD_INPUT,
        },
        SUBMIT: {
            FORM_FIELD_ID: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: WEBFORM_SUBMIT_BUTTON_VALUES,
        },
    },
    ROUND_TIEBREAKER: {
        TEAM_NAME_FIELD: {FORM_FIELD_ID: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FORM_FIELD_ID: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_TIEBREAKER,
        },
        QUESTION: {
            FORM_FIELD_ID: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: QUESTION_NUMBER_HALFTIME_FINAL_TIEBREAKER,
        },
        POINTS: {
            FORM_FIELD_ID: FirstHalfPointBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: VALID_TIEBREAKER_POINTS,
        },
        ANSWER: {FORM_FIELD_ID: AnswerBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        SUBMIT: {
            FORM_FIELD_ID: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: WEBFORM_SUBMIT_BUTTON_VALUES,
        },
    },
}


def Fill_and_submit_trivia_form(data, Send=False):
    # TODO ensure that this function does not fail silently by returning an empty string or None
    """Launch a browser and fill fields of webform then submit.
    The format of the 'data' variable varies based on the form to be filled.
    Round 1 and Round 2 forms are identical differing only in the 'field labels' in use.
    Halftime and FinalRound are the same but use 4 answer boxes. These rounds require
    the 'answer' and 'field' variable to be a list of 4 items each corresponding to
    the box 'field label' and 'answer text' for each of the four answers.
    Tiebrasker round is different in that it only has an answer and no points field.
    Example data dictionary:
    {   TEAM: "My Team Name",
        ROUND: "1",  # values are 1-6, Halftime, Final, Tiebreaker
        QUESTION: "2",  # values are 1-3
        POINTS: "6",  # firstround is 2,4,6  secondround is 5,7,9
        ANSWER: "Place your answer here",
        SUBMIT: True,}  # use False for testing.
    """

    def is_good(value, good_values):
        """Return True if value is part of good_values.
            value and good_values can be a string or list of stings.
            Edgecase: if good_values is equal to FLEXABLE_FIELD_INPUT variable then any reasonably long string of text is allowed.
            Edgecase: if value is a list of strings they should each match the rules for FLEXABLE_FIELD_INPUT
        Args:
            value ([type]): a string or list of strings
            good_values ([type]): a string or list of strings
        Returns: (Bool)
        """
        if good_values == FLEXABLE_FIELD_INPUT: 
            if type(value) == list:
                pass  # TODO check each value for validity
            return True
        if type(value) == str:
            if value in good_values:
                return True
        return False
    
    def is_complete(data, required):
        """Checks 'data' variable for presence of ALL required fields.
            Fields that specify an empty list '[]' are not required.
            Fields that specify 'any' need to be sanitized and restricted to a reasonable length.

        Args:
            data (dict): Should contain ALL the field values to be submitted.
            required (list): Names of ALL fields for this form.

        Returns:
            [bool]: True/False
        """
        return True  # TODO make this work as described.

    browser_token = webdriver.Chrome()
    browser_token.implicitly_wait(2)
    browser_token.get(THE_JOTFORM_URL)
    logger.debug(f'\n{pprint_dicts(data)}')
    # check the supplied data object
    if data[ROUND] in WEBFORM.keys():
        fields_and_functions = WEBFORM[data[ROUND]]
        logger.debug(f'\n{pprint_dicts(fields_and_functions)}')
    else:
        logger.error(f'Bad round name: {data[ROUND]}')
        # CANCEL form submission and inform user.
        browser_token.close()        
        return f'Submit failed. Bad round name: {data[ROUND]}'
    # check the user provided round number/name
    # fill the provided 'Round' value on the form first.
    Round = data.pop(ROUND)
    Submit = data.pop(SUBMIT)  # TODO check this value to be sure it exists and is a bool
    legal_responses = fields_and_functions[ROUND][VALID_RESPONSES]
    if Round in legal_responses:
        logger.debug("Ready to set the round field of form.")
        # the Round field changes the form fields that are available
        fields_and_functions[ROUND][PROPER_FUNCTION](
            browser_token, Round, fields_and_functions[ROUND][FORM_FIELD_ID]
        )
        logger.debug("Round set.")
        sleep(0.5)  # pause to allow page to re-set after round is chosen.
    else:
        logger.error(f"Round: {Round} not found in {legal_responses}")
        # CANCEL form submission and inform user.
        browser_token.close()        
        return f"Submit failed. Acceptable Round values are {legal_responses}"
    # form is now initialized to accept the correct data
    valid_fields = fields_and_functions.keys()
    # TODO check that 'data' has an entry for each required field.
    # Fields that are constrained to an empty list '[]' are not required.
    if is_complete(data, valid_fields) == False:
        logger.error(f'Incomplete data for specified form:\n{pprint_dicts(data)}')
        # CANCEL form submission and inform user.
        browser_token.close()
        return f'Submit failed. Incomplete data for specified form:\n{pprint_dicts(data)}'
    for current_field, value in data.items():
        if current_field in valid_fields:
            legal_responses = fields_and_functions[current_field][VALID_RESPONSES]
            logger.debug(
                f"Field: {current_field} Value: '{value}' Acceptable responses: '{legal_responses}'"
            )
            if is_good(value, legal_responses):
                fields_and_functions[current_field][PROPER_FUNCTION](
                    browser_token, value, fields_and_functions[current_field][FORM_FIELD_ID]
                )
                # TODO error check the browser form
                logger.debug("Field filled.")
            else:
                logger.error(f'Illegal value: {value}')
                # CANCEL form submission and inform user.
                browser_token.close()
                return f'Submit failed. Value: "{value}" for field "{current_field}" is not valid.'
        else:
            logger.error(f"Field: '{current_field}' not found in: '{valid_fields}'")
            # CANCEL form submission and inform user.
            browser_token.close()            
            return f"Submit failed. Input Field: '{current_field}' not found in '{valid_fields}'"
    # Now submit the form if True
    logger.debug("Ready to submit form.")
    legal_responses = fields_and_functions[SUBMIT][VALID_RESPONSES]
    if Submit in legal_responses:
        fields_and_functions[SUBMIT][PROPER_FUNCTION](
            browser_token, Submit, fields_and_functions[SUBMIT][FORM_FIELD_ID]
        )
    else:
        logger.error(f"Submit failed. Value: {Submit} not in {legal_responses}")
        # CANCEL form submission and inform user.
        browser_token.close()        
        return f"Submit failed. Value: {Submit} not in {legal_responses}"
    sleep(0.05)
    browser_token.close()
    data[SUBMIT] = Submit  # place submit field back into dictionary
    data[ROUND] = Round  # place round entry back into dictionary
    return f"Trivia form sent."


@logger.catch
def main():
    # setup some sample answers for testing
    sample_answers = {
        "1": {
            TEAM_NAME_FIELD: "FirstRound",
            ROUND: "1",
            QUESTION: "2",
            POINTS: "6",
            ANSWER: "First round answer",
            SUBMIT: SENDFORM,
        },
        "halftime": {
            TEAM_NAME_FIELD: "Halftime Round",
            ROUND: "Halftime",
            ANSWER: [
                "alpha",
                "beta",
                "delta",
                "gamma",
            ],
            SUBMIT: SENDFORM,
        },
        "4": {
            TEAM_NAME_FIELD: "Second Round",
            ROUND: "4",
            QUESTION: "2",
            POINTS: "9",
            ANSWER: "second round answer",
            SUBMIT: SENDFORM,
        },
        "final": {
            TEAM_NAME_FIELD: "Final Questions",
            ROUND: "Final",
            ANSWER: [
                "alpha",
                "beta",
                "delta",
                "gamma",
            ],
            POINTS: "20",
            SUBMIT: SENDFORM,
        },
        "tiebreaker": {
            TEAM_NAME_FIELD: "Tiebreaker round",
            ROUND: "Tiebreaker",
            ANSWER: "The final decision (no points)",
            SUBMIT: SENDFORM,
        },
        "6": {
            TEAM_NAME_FIELD: "Error Round",
            ROUND: "6",
            QUESTION: "2",
            POINTS: "2",  # this is an error. 2 is not valid in round 6
            ANSWER: "second round answer",
            SUBMIT: SENDFORM,
        },
        "5": {
            TEAM_NAME_FIELD: "Error Round",
            ROUND: "7",  # this is an error. 7 is not valid round.
            QUESTION: "2",
            POINTS: "9",
            ANSWER: "second round answer",
            SUBMIT: SENDFORM,
        },        
        "2": {
            TEAM_NAME_FIELD: "Error Round",  # NOTE: this field is huge on the JotForm
            ROUND: "1",  # this is an error because round and the key for this dict always match.
            QUESTION: "4",  # this is an error. 4 is not valid question number.
            POINTS: "2",
            ANSWER: "second round answer",  # NOTE: this field is also huge
            SUBMIT: SENDFORM,
        },           
    }

    for k, sampleform in sample_answers.items():
        logger.info(f'Sending sample answer #{k}')
        print(Fill_and_submit_trivia_form(sampleform, Send=SENDFORM))
    sleep(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
