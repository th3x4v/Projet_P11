from server import loadClubs
from server import loadCompetitions


def test_loadClubs(clubs):
    """
    Given:the app is launched
    When: the clubs data is extracted from the Json file
    Then: the clubs are properly extracted"""
    extracted_clubs = loadClubs()
    assert len(extracted_clubs) == 3
    assert extracted_clubs[0]["name"] == "Simply Lift"


def test_loadCompetitions(competitions):
    """
    Given:the app is launched
    When: the competition data is extracted from the Json file
    Then: the competitions are properly extracted"""
    extracted_competition = loadCompetitions()
    assert len(extracted_competition) == 2
    assert extracted_competition[0]["name"] == "Spring Festival"
