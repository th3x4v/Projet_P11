from server import clubs, competitions


def test_login_purchase_places(client):
    """
    check if we can successfully purchase places after login
    """

    # login
    response = client.post(
        "/showSummary", data={"email": "john@simplylift.co"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert f"Welcome, john@simplylift.co" in response.data.decode()

    # Book page
    response = client.get("book/Fall%20festival/Simply%20Lift")
    assert response.status_code == 200
    assert "Fall festival" in response.data.decode()
    assert "Book" in response.data.decode()

    # purchasing
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Fall festival", "places": "1"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "booking complete" in response.data.decode()
    assert competitions[2]["numberOfPlaces"] == 4
