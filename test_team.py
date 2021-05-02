from team import Team

def test_creating_a_team_sets_defaults():
    team = Team("Test Team")

    assert team.name == "Test Team"
    assert team.round == 1
    assert team.question == 1

def test_team_tracks_the_current_question_and_available_points():
    team = Team("Test Team")

    resp = team.submit_answer(4)

    assert resp == True
    assert team.round == 1
    assert team.question == 2
    assert team.spent_points == [4]

def test_team_returns_False_if_point_value_was_already_used_this_round():
    team = Team("Test Team")

    team.submit_answer(4)
    resp = team.submit_answer(4)

    assert resp == False

def test_team_transitions_rounds_automatically():
    team = Team("Test Team")

    team.submit_answer(2)
    team.submit_answer(4)
    team.submit_answer(6)

    assert team.round == 2
    assert team.question == 1

def test_team_transitions_to_halftime():
    team = Team("Test Team")
    team.round = 3
    team.question = 3

    team.submit_answer(4)

    assert team.round == 'halftime'
    assert team.question == 1

def test_team_transitions_to_final():
    team = Team("Test Team")
    team.round = 6
    team.question = 3
    team.submit_answer(9)

    assert team.round == 'final'
    assert team.question == 1

def test_team_transitions_to_tiebreaker():
    team = Team("Test Team")
    team.round = 'final'
    team.submit_answer(20)

    assert team.round == 'tiebreaker'
    assert team.question == 1

def test_team_validates_points_based_on_round():
    team = Team("Test Team")

    resp = team.submit_answer(5)
    assert resp == False
    resp = team.submit_answer(4)
    assert resp == True

    team.round = 4
    resp = team.submit_answer(2)
    assert resp == False
    resp = team.submit_answer(7)
    assert resp == True

    team.round = 'final'
    resp = team.submit_answer(21)
    assert resp == False
    resp = team.submit_answer(20)
    assert resp == True

def test_get_team_by_name():
    team1 = Team("Test Team 1")
    team2 = Team("Test Team 2")

    result = Team.get_team_by_name("Test Team 2")
    
    assert result == team2

def test_get_team_by_name_returns_None_if_no_team_exists():
    team1 = Team("Test Team 1")

    result = Team.get_team_by_name("Fish")

    assert result is None