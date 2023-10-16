import pytest


def test_showSummary_known_email_response_code(client):
    """
    Given: A user access show summary
    When: he input a known email
    Then: we receive a status_code 200
    """
    email = "admin@irontemple.com"
    response = client.post("/showSummary", data={"email": email})
    assert response.status_code == 200


def test_showSummary_unknown_email(client):
    """
    Given: A user access show summary
    When: he input an unknown email
    Then: we are redirected to the index page with an error message
    """
    email = "test@mail.com"
    response = client.post("/showSummary", data={"email": email})
    assert response.status_code == 302
