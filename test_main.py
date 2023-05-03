'''
Tests for jwt flask app.
'''
import os
import json
import pytest

import main

SECRET = 'TestSecret'
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjEzMDY3OTAsIm5iZiI6MTU2MDA5NzE5MCwiZW1haWwiOiJ3b2xmQHRoZWRvb3IuY29tIn0.IpM4VMnqIgOoQeJxUbLT-cRcAjK41jronkVrqRLFmmk'
EMAIL = 'wolf@thedoor.com'
PASSWORD = 'huff-puff'

@pytest.fixture
def client():
    os.environ['JWT_SECRET'] = SECRET
    main.APP.config['TESTING'] = True
    client = main.APP.test_client()

    yield client



def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == 'Healthy'


def test_auth(client):
    body = {'email': EMAIL,
            'password': PASSWORD}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')

    assert response.status_code == 200
    token = response.json['token']
    assert token is not None

# import json
import unittest
from main import APP


class TestApp(unittest.TestCase):

    def setUp(self):
        APP.testing = True
        self.client = APP.test_client()

    def test_health(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), "Healthy")

    def test_auth_missing_email(self):
        data = {'password': 'mypassword'}
        response = self.client.post('/auth', json=data)
        self.assertEqual(response.status_code, 200)

    def test_auth_missing_password(self):
        data = {'email': 'user@example.com'}
        response = self.client.post('/auth', json=data)
        self.assertEqual(response.status_code, 200)

    def test_auth_valid_credentials(self):
        data = {'email': 'user@example.com', 'password': 'mypassword'}
        response = self.client.post('/auth', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(json.loads(response.data)['token'])

    def test_decode_jwt_no_auth_header(self):
        response = self.client.get('/contents')
        self.assertEqual(response.status_code, 401)

    def test_decode_jwt_invalid_token(self):
        headers = {'Authorization': 'Bearer invalidtoken'}
        response = self.client.get('/contents', headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_decode_jwt_valid_token(self):
        data = {'email': 'user@example.com', 'password': 'mypassword'}
        auth_response = self.client.post('/auth', json=data)
        token = json.loads(auth_response.data)['token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.get('/contents', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['email'], 'user@example.com')

if __name__ == "__main__":
    unittest.main()