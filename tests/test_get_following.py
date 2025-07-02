import pytest
from main import app as flask_app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

@patch("services.functions.conection_userprofile")
@patch("jwt.decode")
def test_get_following_success(mock_jwt_decode, mock_conection, client):
    mock_jwt_decode.return_value = {"user_id": 1}

    mock_session = MagicMock()
    mock_conection.return_value = mock_session

    # Mock profile exists
    profile_mock = MagicMock()
    profile_mock.Id_User = 2
    profile_mock.User_mail = "test@example.com"
    mock_session.query().filter_by().first.return_value = profile_mock

    # Mock following list
    following_mock = [profile_mock]
    mock_session.query().join().filter().all.return_value = following_mock

    headers = {"Authorization": "Bearer fake-token"}
    response = client.get("/following", headers=headers)

    assert response.status_code == 200
    assert response.json == {
        "following": [
            {
                "Id_User": 2,
                "User_mail": "test@example.com"
            }
        ]
    }
