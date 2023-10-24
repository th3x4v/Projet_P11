def test_login_purchase_places(client, clubs, competitions_availability, monkeypatch):
    """
    check if we can successfully purchase places after login
    """
    monkeypatch.setattr("server.competitions", competitions_availability)
    monkeypatch.setattr("server.clubs", clubs)
    club = clubs[0]
    competition = competitions_availability[2]

    # login
    response = client.post(
        "/showSummary", data={"email": club["email"]}, follow_redirects=True
    )
    assert response.status_code == 200
    assert f"Welcome, {club['email']}" in response.data.decode()

    # Book page
    response = client.get("book/Fall%20festival/Simply%20Lift")
    assert response.status_code == 200
    assert "Fall festival" in response.data.decode()
    assert "Book" in response.data.decode()

    # purchasing
    response = client.post(
        "/purchasePlaces",
        data={"club": club["name"], "competition": competition["name"], "places": "1"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "booking complete" in response.data.decode()
    assert competition["numberOfPlaces"] == 4
