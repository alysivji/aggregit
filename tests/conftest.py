import json

import pytest

from app import app


@pytest.fixture(scope='session')
def _client():
    app.testing = True
    return app.test_client()


@pytest.fixture(scope='session')
def client(_client):
    """
    Fixture that hits Flask test client and deserializes JSON

    Returns
    -------
    dict
        Deserialized JSON from Response
    """
    def _dejsonify(endpoint):
        result = _client.get(endpoint)
        return json.loads(result.data)
    return _dejsonify
