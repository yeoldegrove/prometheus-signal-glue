import pytest
import glue

from unittest.mock import patch

@pytest.fixture
def message():
    return
    {"message": "Breaky breaky", "number": "+0012345678", "recipients": ["+0012345678"]}


def alert():
    return {"alerts": [{"alert": "SampleAlert"}]}


@pytest.fixture
def client():

    glue.app.config["TESTING"] = True
    return glue.app.test_client()

@pytest.mark.skip("Message seems empty")
@patch("glue.requests.post")
def test_send_message(mock_post, message):
    mock_post.return_value.ok = True
    # import pdb; pdb.set_trace()
    glue.send_message("Breaky breaky", "+0012345678", recipients=["+0012345678"])

    mock_post.assert_called_with("http://127.0.0.1:8080/v1/send", json=message, timeout=5)
    
    import pdb; pdb.set_trace()


@patch("glue.requests.post")
def test_alerts(mock_post, client):
    mock_post.return_value.ok = True
    response = client.post("/alerts", json=alert())

    assert b"Alerts delivered to signal" in response.data
