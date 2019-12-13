from django.test import TestCase
from rest_framework.test import RequestsClient
from django.contrib.auth.models import User

# Create your tests here.
class Authentification_Tests(TestCase):
    def test_non_authorizied_access(self):
        """
            Test an unauthorized access to all endpoints

            Note :
                request the endpoints
                checks the response's code

        """
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/v1.0/output/roadgrade')
        assert response.status_code == 401
        response = client.get('http://127.0.0.1:8000/api/v1.0/output/trustrate')
        assert response.status_code == 401

    def test_authorized_access(self):
        """
            Test an authorized access to all endpoints

            Note :
                creates a user
                request the login endpoint of the app
                gets the token
                request the endpoints and checks the response's code

        """
        client = RequestsClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        params = {'username': 'testuser', 'password': '12345'}
        response = client.post('http://127.0.0.1:8000/api/token/', params)
        json_array = response.json()
        header = {
            "Authorization": "Bearer " + json_array['access']
        }
        response = client.get('http://127.0.0.1:8000/api/v1.0/output/roadgrade', headers = header)
        assert response.status_code == 200
        response = client.get('http://127.0.0.1:8000/api/v1.0/output/roadgrade', headers=header)
        assert response.status_code == 200