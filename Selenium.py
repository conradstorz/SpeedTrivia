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
SENDFORM = True  # Control the behaviour of the sample values during testing.
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

FIELD_KEY = "fld"
PROPER_FUNCTION = "func"
VALID_RESPONSES = "valid_response"
ROUND = "round"
SUBMIT = "submit"
TEAM_KEY = "team"

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


ROUND_FIELD_VALUES = [
    "1",
    "2",
    "3",
    "Halftime",
    "4",
    "5",
    "6",
    "Final",
    "Tiebreaker",
]
FLEXABLE_FIELD_INPUT = "any"  # Flag to indicate any reasonable text can be input.
QUESTION = "question"
POINTS = "points"
ANSWER = "answer"
WEBFORM = {
    "1": {
        TEAM_KEY: {FIELD_KEY: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FIELD_KEY: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_FIELD_VALUES,
        },
        QUESTION: {
            FIELD_KEY: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ["1", "2", "3"],
        },
        POINTS: {
            FIELD_KEY: FirstHalfPointBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ["2", "4", "6"],
        },
        ANSWER: {FIELD_KEY: AnswerBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        SUBMIT: {
            FIELD_KEY: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: [True, False],
        },
    },
    "2": {
        TEAM_KEY: {FIELD_KEY: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FIELD_KEY: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_FIELD_VALUES,
        },
        QUESTION: {
            FIELD_KEY: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ["1", "2", "3"],
        },
        POINTS: {
            FIELD_KEY: FirstHalfPointBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ["2", "4", "6"],
        },
        ANSWER: {FIELD_KEY: AnswerBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        SUBMIT: {
            FIELD_KEY: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: [True, False],
        },
    },
    "3": {
        TEAM_KEY: {FIELD_KEY: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FIELD_KEY: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_FIELD_VALUES,
        },
        QUESTION: {
            FIELD_KEY: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ["1", "2", "3"],
        },
        POINTS: {
            FIELD_KEY: FirstHalfPointBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ["2", "4", "6"],
        },
        ANSWER: {FIELD_KEY: AnswerBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        SUBMIT: {
            FIELD_KEY: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: [True, False],
        },
    },
    "Halftime": {
        TEAM_KEY: {FIELD_KEY: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FIELD_KEY: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_FIELD_VALUES,
        },
        QUESTION: {
            FIELD_KEY: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: [],
        },
        POINTS: {
            FIELD_KEY: FirstHalfPointBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: [],
        },
        ANSWER: {
            FIELD_KEY: HalftimeAndFinalAnswerBoxIDs,
            PROPER_FUNCTION: Fill_four_answers,
            VALID_RESPONSES: FLEXABLE_FIELD_INPUT,
        },
        SUBMIT: {
            FIELD_KEY: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: [True, False],
        },
    },
    "4": {
        TEAM_KEY: {FIELD_KEY: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FIELD_KEY: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_FIELD_VALUES,
        },
        QUESTION: {
            FIELD_KEY: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ["1", "2", "3"],
        },
        POINTS: {
            FIELD_KEY: SecondHalfPointBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ["5", "7", "9"],
        },
        ANSWER: {FIELD_KEY: AnswerBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        SUBMIT: {
            FIELD_KEY: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: [True, False],
        },
    },
    "5": {
        TEAM_KEY: {FIELD_KEY: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FIELD_KEY: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_FIELD_VALUES,
        },
        QUESTION: {
            FIELD_KEY: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ["1", "2", "3"],
        },
        POINTS: {
            FIELD_KEY: SecondHalfPointBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ["5", "7", "9"],
        },
        ANSWER: {FIELD_KEY: AnswerBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        SUBMIT: {
            FIELD_KEY: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: [True, False],
        },
    },
    "6": {
        TEAM_KEY: {FIELD_KEY: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FIELD_KEY: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_FIELD_VALUES,
        },
        QUESTION: {
            FIELD_KEY: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ["1", "2", "3"],
        },
        POINTS: {
            FIELD_KEY: SecondHalfPointBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ["5", "7", "9"],
        },
        ANSWER: {FIELD_KEY: AnswerBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        SUBMIT: {
            FIELD_KEY: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: [True, False],
        },
    },
    "Final": {
        TEAM_KEY: {FIELD_KEY: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FIELD_KEY: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_FIELD_VALUES,
        },
        QUESTION: {
            FIELD_KEY: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: [],
        },
        POINTS: {
            FIELD_KEY: FinalQuestionWagerID,
            PROPER_FUNCTION: Fill_a_field,
            VALID_RESPONSES: [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
            ],
        },
        ANSWER: {
            FIELD_KEY: HalftimeAndFinalAnswerBoxIDs,
            PROPER_FUNCTION: Fill_four_answers,
            VALID_RESPONSES: FLEXABLE_FIELD_INPUT,
        },
        SUBMIT: {
            FIELD_KEY: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: [True, False],
        },
    },
    "Tiebreaker": {
        TEAM_KEY: {FIELD_KEY: TeamNameBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        ROUND: {
            FIELD_KEY: GameRoundBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: ROUND_FIELD_VALUES,
        },
        QUESTION: {
            FIELD_KEY: GameQuestionBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: [],
        },
        POINTS: {
            FIELD_KEY: FirstHalfPointBoxID,
            PROPER_FUNCTION: Fill_a_dropdown,
            VALID_RESPONSES: [],
        },
        ANSWER: {FIELD_KEY: AnswerBoxID, PROPER_FUNCTION: Fill_a_field, VALID_RESPONSES: FLEXABLE_FIELD_INPUT},
        SUBMIT: {
            FIELD_KEY: SubmitButtonID,
            PROPER_FUNCTION: Click_a_button,
            VALID_RESPONSES: [True, False],
        },
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
    {   TEAM: "My Team Name",
        ROUND: "1",  # values are 1-6, Halftime, Final, Tiebreaker
        QUESTION: "2",  # values are 1-3
        POINTS: "6",  # firstround is 2,4,6  secondround is 5,7,9
        ANSWER: "Place your answer here",
        SUBMIT: True,}  # use False for testing.
    """
    browser_token = webdriver.Chrome()
    browser_token.implicitly_wait(10)
    browser_token.get(THE_JOTFORM_URL)
    fields_and_functions = WEBFORM[data[ROUND]]
    logger.debug(fields_and_functions)
    logger.debug("...")
    logger.debug(data)
    # fill the 'Round' value on the form first.
    Round = data.pop(ROUND)
    Submit = data.pop(SUBMIT)
    legal_responses = fields_and_functions[ROUND][VALID_RESPONSES]
    if Round in legal_responses:
        logger.debug("Ready to set the round field of form.")
        fields_and_functions[ROUND][PROPER_FUNCTION](
            browser_token, Round, fields_and_functions[ROUND][FIELD_KEY]
        )
        logger.debug("Round set.")
        sleep(0.5)  # pause to allow page to re-set after round is chosen.
    else:
        logger.error(f"Round: {Round} not found in {legal_responses}")
        return f"Acceptable Round values are {legal_responses}"
    # form is now initialized to accept the correct data
    valid_fields = fields_and_functions.keys()
    for current_field, value in data.items():
        if current_field in valid_fields:
            legal_responses = fields_and_functions[current_field][VALID_RESPONSES]
            # TODO validate that the value is acceptable for the field it is being offered.
            # if value_is_acceptable(value, legal_values):
            # proceede
            # else log error
            logger.debug(
                f"Field: {current_field} Value: {value} Acceptable responses: {legal_responses}"
            )
            fields_and_functions[current_field][PROPER_FUNCTION](
                browser_token, value, fields_and_functions[current_field][FIELD_KEY]
            )
            # TODO error check the browser form
            logger.debug("Field filled.")
        else:
            logger.error(f"Field: {current_field} not found in: {valid_fields}")
            return f"Input Field: {current_field} not found in {valid_fields}"
    # Now submit the form if True
    logger.debug("Ready to submit form.")
    legal_responses = fields_and_functions[SUBMIT][VALID_RESPONSES]
    if Submit in legal_responses:
        fields_and_functions[SUBMIT][PROPER_FUNCTION](
            browser_token, Submit, fields_and_functions[SUBMIT][FIELD_KEY]
        )
    else:
        logger.error(f"Submit failed. Value: {Submit} not in {legal_responses}")
        return "Submit of form failed."
    sleep(0.5)
    browser_token.close()
    data[SUBMIT] = Submit  # place submit field back into dictionary
    data[ROUND] = Round  # place round entry back into dictionary
    return f"Trivia form sent:\n{pprint_dicts(data)}"


@logger.catch
def main():
    # setup some sample answers for testing
    sample_answers = {
        "1": {
            TEAM_KEY: "FirstRound",
            ROUND: "1",
            QUESTION: "2",
            POINTS: "6",
            ANSWER: "First round answer",
            SUBMIT: SENDFORM,
        },
        "halftime": {
            TEAM_KEY: "Halftime Round",
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
            TEAM_KEY: "Second Round",
            ROUND: "4",
            QUESTION: "2",
            POINTS: "9",
            ANSWER: "second round answer",
            SUBMIT: SENDFORM,
        },
        "final": {
            TEAM_KEY: "Final Questions",
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
            TEAM_KEY: "Tiebreaker round",
            ROUND: "Tiebreaker",
            ANSWER: "The final decision (no points)",
            SUBMIT: SENDFORM,
        },
        "6": {
            TEAM_KEY: "Second Round",
            ROUND: "6",
            QUESTION: "2",
            POINTS: "2",  # this is an error. 2 is not valid in round 6
            ANSWER: "second round answer",
            SUBMIT: SENDFORM,
        },
    }

    for k, sampleform in sample_answers.items():
        Fill_and_submit_trivia_form(sample_answers[k], Send=False)
    sleep(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
