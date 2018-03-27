import json


def test_github_user_does_not_exist(_client, mocker):
    """
    Try to find Github user that does not exist, should return 404
    """
    # Arrange
    mock_response = mocker.MagicMock(name='Mock response')
    mock_response.json.return_value = {
        "message": "Not Found",
        "documentation_url": "https://developer.github.com/v3/users/#get-a-single-user"  # noqa
    }

    mock_requests = mocker.patch('app.adapters.github.requests')
    mock_requests.get.return_value = mock_response

    # Act
    username = "name_does_not_exist"
    result = _client.get(f'/api/v1/github/{username}')

    # Assert
    assert result.status_code == 404

    json_result = json.loads(result.data)
    assert json_result['error'] == 'Github ID not found'


def test_bitbucket_user_does_not_exist(_client, mocker):
    # Arrange
    mock_response = mocker.MagicMock(name='Mock response')
    mock_response.json.return_value = {
        "type": "error",
        "error": {
            "message": "name_does_not_exist"
        }
    }

    mock_requests = mocker.patch('app.adapters.bitbucket.requests')
    mock_requests.get.return_value = mock_response

    # Act
    username = "name_does_not_exist"
    result = _client.get(f'/api/v1/bitbucket/{username}')

    # Assert
    assert result.status_code == 404

    json_result = json.loads(result.data)
    assert json_result['error'] == 'BitBucket ID not found'
