"""
Tests for BitBucket Adapter
"""

import os

import app.adapters.bitbucket as bitbucket

CWD = os.path.dirname(__file__)


# TODO monkey-patching versus dependency injection. I like the Java mindset of
# DI, but monkey-patching is quick and dirty for coding assessments
# Discuss further in code review

def test_fetch_user_data(mocker, json_loader):
    """
    Test getting data for team accounts
    """
    # Arrange
    user_account_data = json_loader(os.path.join(CWD, 'users_response.json'))

    mock_response = mocker.MagicMock(name='Mock response')
    mock_response.json.return_value = user_account_data

    mock_requests = mocker.patch('app.adapters.bitbucket.requests')
    mock_requests.get.return_value = mock_response

    # Act
    resp = bitbucket.fetch_user_data('test_user')

    # Assert
    assert resp == user_account_data


def test_fetch_user_data_for_team_account(mocker, json_loader):
    """
    Test getting data for team accounts
    """
    # Arrange
    team_account_message = {
        "type": "error",
        "error": {
            "message": "pygame is a team account"
        }
    }
    team_account_data = json_loader(os.path.join(CWD, 'teams_response.json'))

    mock_response = mocker.MagicMock(name='Mock response')
    mock_response.json.side_effect = [team_account_message, team_account_data]

    mock_requests = mocker.patch('app.adapters.bitbucket.requests')
    mock_requests.get.return_value = mock_response

    # Act
    resp = bitbucket.fetch_user_data('test_user')

    # Assert
    assert resp == team_account_data
