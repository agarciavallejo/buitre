import os
import tempfile
import pytest

from Backend.src.main import app

@pytest.fixture
def client():
	db_fd, app.config['DATABASE'] = tempfile.mkstemp()
	app.config['TESTING'] = True
	client = app.test_client()

	with app.app_context():
		app.init_db()

	yield client

	os.close(db_fd)
	os.unlink(app.config['DATABASE'])

def test_dummy(client):
	""" blank database """
	rv = client.get('/')
	assert b'something' in rv.data