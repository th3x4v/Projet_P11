from server import is_competition_available
from freezegun import freeze_time


@freeze_time("2012-01-14")
def test_sets_available_key_to_true_if_date_is_in_future(competitions):
    result = is_competition_available(competitions[0])
    assert result["available"] == True


@freeze_time("2025-01-14")
def test_sets_available_key_to_true_if_date_is_in_future(competitions):
    result = is_competition_available(competitions[0])
    assert result["available"] == False


def test_book_competition_without_availability(
    client, clubs, competitions_availability, monkeypatch
):
    """
    Given: a user try to access a competition
    When:
    Then:
    """
    monkeypatch.setattr("server.competitions", competitions_availability)
    monkeypatch.setattr("server.clubs", clubs)
    response = client.get("book/Spring%20Festival/Simply%20Lift")
    assert response.status_code == 200
    assert b"This competition is not available" in response.data


def test_book_valid_competition(client, clubs, competitions_availability, monkeypatch):
    """
    Given: A user access the booking feature for a competition
    When: a competition is in the future
    Then: he should be redirected to the correct booking template
    """
    monkeypatch.setattr("server.competitions", competitions_availability)
    monkeypatch.setattr("server.clubs", clubs)
    response = client.get("book/Fall%20festival/Simply%20Lift")
    assert response.status_code == 200
