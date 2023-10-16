import pytest


def test_purchase_places_and_deduct_points(client, clubs, competitions, monkeypatch):
    """
    Given: User tries to retrieve 5 places for a competition.
    When: User books 5 places.
    Then: Number of places available for the competition decreases from 25 to 20 and the number of points available decreases from 13 to 8.
    """
    monkeypatch.setattr("server.competitions", competitions)
    monkeypatch.setattr("server.clubs", clubs)
    # competition to book
    competition = competitions[0]
    # booker club
    club = clubs[0]

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition["name"],
            "club": club["name"],
            "places": 5,
        },
    )

    assert competitions[0]["numberOfPlaces"] == 20
    assert clubs[0]["points"] == 8
    assert response.status_code == 200
