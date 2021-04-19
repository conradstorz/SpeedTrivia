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
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown},
        "points": {"fld": FirstHalfPointBoxID, "func": Fill_a_dropdown},
        "answer": {"fld": AnswerBoxID, "func": Fill_a_field},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button},
    },
    "2": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown},
        "points": {"fld": FirstHalfPointBoxID, "func": Fill_a_dropdown},
        "answer": {"fld": AnswerBoxID, "func": Fill_a_field},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button},
    },
    "3": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown},
        "points": {"fld": FirstHalfPointBoxID, "func": Fill_a_dropdown},
        "answer": {"fld": AnswerBoxID, "func": Fill_a_field},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button},
    },
    "Halftime": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown},
        "points": {"fld": FirstHalfPointBoxID, "func": Fill_a_dropdown},
        "answer": {"fld": HalftimeAndFinalAnswerBoxIDs, "func": Fill_four_answers},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button},
    },
    "4": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown},
        "points": {"fld": SecondHalfPointBoxID, "func": Fill_a_dropdown},
        "answer": {"fld": AnswerBoxID, "func": Fill_a_field},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button},
    },
    "5": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown},
        "points": {"fld": SecondHalfPointBoxID, "func": Fill_a_dropdown},
        "answer": {"fld": AnswerBoxID, "func": Fill_a_field},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button},
    },
    "6": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown},
        "points": {"fld": SecondHalfPointBoxID, "func": Fill_a_dropdown},
        "answer": {"fld": AnswerBoxID, "func": Fill_a_field},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button},
    },
    "Final": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown},
        "points": {"fld": FinalQuestionWagerID, "func": Fill_a_field},
        "answer": {"fld": HalftimeAndFinalAnswerBoxIDs, "func": Fill_four_answers},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button},
    },
    "Tiebreaker": {
        "team": {"fld": TeamNameBoxID, "func": Fill_a_field},
        "round": {"fld": GameRoundBoxID, "func": Fill_a_dropdown},
        "question": {"fld": GameQuestionBoxID, "func": Fill_a_dropdown},
        "points": {"fld": FirstHalfPointBoxID, "func": Fill_a_dropdown},
        "answer": {"fld": AnswerBoxID, "func": Fill_a_field},
        "submit": {"fld": SubmitButtonID, "func": Click_a_button},
    },
}

SENDFORM = False
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


def Fill_and_submit_trivia_form(data):
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
    web = webdriver.Chrome()
    web.get("https://form.jotform.com/202575177230149")
    fields_and_functions = WEBFORM[data["round"]]
    logger.debug(fields_and_functions)
    logger.debug("...")
    logger.debug(data)
    # fill the 'Round' value on the form first.
    Round = data.pop("round")
    fields_and_functions["round"]["func"](
        web, Round, fields_and_functions["round"]["fld"]
    )
    # form is now initialized to accept the correct data
    for field, value in data.items():
        logger.debug(f"Field: {field} Value: {value}")
        if field in fields_and_functions.keys():
            fields_and_functions[field]["func"](
                web, value, fields_and_functions[field]["fld"]
            )
    sleep(10)
    web.close()
    return "Trivia form sent."


@logger.catch
def main():
    for k, sampleform in sample_answers.items():
        Fill_and_submit_trivia_form(sample_answers[k])
    sleep(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
