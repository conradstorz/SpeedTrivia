from Webform_filler import parse_tracked_answer, determine_answer_format, Check_for_webform_answer_submission
from team import Team

def test_parse_tracked_answer_with_standard_round_question():
    team = Team("Test Team")
    sms_body = "4 Test"
    data = parse_tracked_answer(team, sms_body, True)

    expected = {
        "team": "Test Team",
        "round": "1",
        "question": "1",
        "points": "4",
        "answer": "Test",
        "submit": True,
    }

    assert data == expected

def test_parse_tracked_answer_with_halftime_question():
    team = Team("Test Team")
    assert False

def test_skipped_question_adjusts_to_new_round_and_question():
    assert False

def test_parse_tracked_answer_with_final_question():
    assert False

def test_parse_precise_answer_with_standard_round_question():
    assert False

def test_parse_precise_answer_with_halftime_question():
    assert False

def test_parse_precise_answer_with_final_question():
    assert False

def test_submitting_a_precise_answer_updates_the_Team():
    assert False

def test_determine_answer_format_with_precise_answer():
    sms_body = "R4Q1P7AFish"

    fmt = determine_answer_format(sms_body)

    assert fmt == "precise"

def test_determine_answer_format_with_tracked_answer():
    sms_body = "7 Fish"

    fmt = determine_answer_format(sms_body)

    assert fmt == "tracked"

def test_determine_answer_format_with_gibberish():
    sms_body = "alsdkfjasdinag"

    fmt = determine_answer_format(sms_body)

    assert fmt == "unrecognized"

def test_Check_for_webform_answer_submission_with_precise_answer(mocker):
    # Check_for_webform_answer_submission(msid, sms_from, body_of_sms, teamname, Send=False)
    mocked = mocker.patch('Webform_filler.Fill_and_submit_trivia_form')
    mocked.return_value = "Called fill and submit"
    sms_body = 'R3Q1P4AFish'
    expected_data = {
        "team": "Test Team",
        "round": "3",
        "question": "1",
        "points": "4",
        "answer": "Fish",
        "submit": True,
    }

    res = Check_for_webform_answer_submission(1, '+15551234567', sms_body, 'Test Team', True)

    mocked.assert_called_once_with(expected_data, Send=True)
    assert res == "Called fill and submit"

def test_Check_for_webform_answer_submission_with_tracked_answer(mocker):
    mocked = mocker.patch('Webform_filler.Fill_and_submit_trivia_form')
    mocked.return_value = "Called fill and submit"
    sms_body = '4 Fish'
    team = Team("Test Team")

    expected_data = {
        "team": "Test Team",
        "round": "1",
        "question": "1",
        "points": "4",
        "answer": "Fish",
        "submit": True,
    }

    res = Check_for_webform_answer_submission(1, '+15551234567', sms_body, 'Test Team', True)

    mocked.assert_called_once_with(expected_data, Send=True)
    assert res == "Called fill and submit"

def test_Check_for_webform_answer_submission_with_gibberish():
    #result = "Did not recognize a trivia answer."  # no response to the sender
    sms_body = 'asdkfjaskdfja'
    res = Check_for_webform_answer_submission(1, '+15551234567', sms_body, 'Test Team', True)
    assert res == "Did not recognize a trivia answer."