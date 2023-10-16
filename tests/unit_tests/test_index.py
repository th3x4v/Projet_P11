import pytest


def test_index(client):
    """
    Given: A user access the site
    When: he access the index url
    Then: we receive a status code 200
    """
    response = client.get("/")
    assert response.status_code == 200


def test_logout(client):
    """
    Given: A user access the site
    When: they access the logout url
    Then: we expect a status code of 302
    """
    response = client.get("/logout")
    assert response.status_code == 302
