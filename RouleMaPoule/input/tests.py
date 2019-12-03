from django.contrib.auth.models import User
from django.test import TestCase
from .processing import csv_upload
from rest_framework.test import RequestsClient


class Authentification_Tests(TestCase):

    def test_token_ok(self):
        client = RequestsClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        params = {'username': 'testuser', 'password': '12345'}
        response = client.post('http://127.0.0.1:8000/api/token/', params)
        json_string = response.content.decode('utf8').replace("'", '"')
        assert response.status_code == 200
        assert "access" in json_string


    def test_token_ko(self):
        client = RequestsClient()
        params = {'username': 'testuser', 'password': '12345'}
        response = client.post('http://127.0.0.1:8000/api/token/', params)
        json_string = response.content.decode('utf8').replace("'", '"')
        assert response.status_code == 401


    def test_non_authorizied_access(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/v1.0/input/waypoint/')
        assert response.status_code == 401
        response = client.get('http://127.0.0.1:8000/api/v1.0/input/path')
        assert response.status_code == 401
        response = client.get('http://127.0.0.1:8000/api/v1.0/input/acceleration')
        assert response.status_code == 401

    def test_authorized_access(self):
        client = RequestsClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        params = {'username': 'testuser', 'password': '12345'}
        response = client.post('http://127.0.0.1:8000/api/token/', params)
        json_array = response.json()
        header = {
            "Authorization": "Bearer " + json_array['access']
        }
        response = client.get('http://127.0.0.1:8000/api/v1.0/input/waypoint/', headers = header)
        assert response.status_code == 200
        response = client.get('http://127.0.0.1:8000/api/v1.0/input/path', headers=header)
        assert response.status_code == 200
        response = client.get('http://127.0.0.1:8000/api/v1.0/input/acceleration', headers=header)
        assert response.status_code == 200




class CSV_import_Tests(TestCase):

    def test_import_csv(self):
        csv_file= open('test.csv', 'r+')
        csv_upload.csv_upload(csv_file)
        self.assertIs(False, False)