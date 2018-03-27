import json

import pytest

from app import app


@pytest.fixture(scope='session')
def client():
    app.testing = True
    return app.test_client()


@pytest.fixture(scope='session')
@pytest.fixture
def json_loader():
    """
    Loads data from JSON file
    """
    def _loader(filename):
        with open(filename, 'r') as f:
            print(filename)
            data = json.load(f)
        return data

    return _loader
