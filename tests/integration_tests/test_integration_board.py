from server import clubs, competitions


def test_login_board(client, clubs, competitions_availability, monkeypatch):
    """
    check if we can successfully purchase places after login
    """

    # login
    response = client.post(
        "/showSummary", data={"email": "john@simplylift.co"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert f"Welcome, john@simplylift.co" in response.data.decode()

    # board page
    response = client.get("board")
    assert response.status_code == 200
    assert "display board" in response.data.decode()

    # back to summary page
    response = client.get("/showSummary?club=Simply+Lift", follow_redirects=True)
    assert response.status_code == 200
    assert f"Welcome, john@simplylift.co" in response.data.decode()
