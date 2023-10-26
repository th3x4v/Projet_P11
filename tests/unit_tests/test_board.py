def test_board(client, clubs, monkeypatch):
    """
    GIVEN a request on the board page
    WHEN the '/board' page get the request (GET)
    THEN check is the status code returned is 200, and if a text is in the response. Check if correct clubs/amounts of points displays correctly
    """
    monkeypatch.setattr("server.clubs", clubs)
    response = client.get("/board")
    assert response.status_code == 200
    assert clubs[0]["name"] in response.data.decode()
    assert clubs[0]["points"] in response.data.decode()


def test_board_public(client, clubs, monkeypatch):
    """
    GIVEN a request on the board page
    WHEN the '/board' page get the request (GET)
    THEN check is the status code returned is 200, and if a text is in the response. Check if correct clubs/amounts of points displays correctly
    """
    monkeypatch.setattr("server.clubs", clubs)
    response = client.get("/boardpublic")
    assert response.status_code == 200
    assert clubs[0]["name"] in response.data.decode()
    assert clubs[0]["points"] in response.data.decode()
