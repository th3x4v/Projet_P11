def test_login_board(client, clubs, competitions_availability, monkeypatch):
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

    # board page
    response = client.get("board")
    assert response.status_code == 200
    assert "display board" in response.data.decode()

    # back to summary page
    response = client.get("/showSummary?club=" + club["name"], follow_redirects=True)
    assert response.status_code == 200
    assert f"Welcome, {club['email']}" in response.data.decode()
