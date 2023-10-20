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


def test_purchasePlaces_customer_book_too_many_places(
    client, clubs, competitions, monkeypatch
):
    """Scenario: A customer tries to book more places for a competition than allowed.

    Given: A user want to book places for a competition.
    When: The user attempts to book 13 places.
    Then: We expect a 200 status code, an error message indicating the booking limit, and no modification to the number of places or points.
    """
    monkeypatch.setattr("server.competitions", competitions)
    monkeypatch.setattr("server.clubs", clubs)

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions[0]["name"],
            "club": clubs[0]["name"],
            "places": 13,
        },
    )
    assert response.status_code == 200
    assert b"You cannot book more than 12 places for a competition" in response.data
    assert int(competitions[0]["numberOfPlaces"]) == 25
    assert int(clubs[0]["points"]) == 13


def test_purchasePlaces_customer_not_have_enough_places(
    client, clubs, competitions, monkeypatch
):
    """
    Scenario: A customer attempts to book places without having enough points.

    Given: A user with 4 points want to book places for a competition.
    When: The user attempts to book 6 places.
    Then: We expect a 200 status code, an error message indicating insufficient points, and no modification to the number of places or points.
    """
    monkeypatch.setattr("server.competitions", competitions)
    monkeypatch.setattr("server.clubs", clubs)

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions[0]["name"],
            "club": clubs[1]["name"],
            "places": 6,
        },
    )
    assert response.status_code == 200
    assert b"have enough points (4) to reedem 6 places" in response.data
    assert int(competitions[0]["numberOfPlaces"]) == 25
    assert int(clubs[1]["points"]) == 4
