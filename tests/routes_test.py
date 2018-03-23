import json

import pytest

from app import app


@pytest.fixture
def _client():
    app.testing = True
    return app.test_client()


@pytest.fixture
def client(_client):
    """
    Fixture that hits Flask test client and deserializes JSON

    Returns
    -------
    dict
        Deserialized JSON from Request
    """
    def _dejsonify(endpoint):
        result = _client.get('/')
        return json.loads(result.data)
    return _dejsonify


def test_index(client):
    result = client('/')

    assert isinstance(result, list)
