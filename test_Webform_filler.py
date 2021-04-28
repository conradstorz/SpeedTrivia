from Webform_filler import parse_tracked_answer
from team import Team

def test_parse_tracked_answer():
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