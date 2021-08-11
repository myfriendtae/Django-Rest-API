from django.test import TestCase, client
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_URER_URL = reverse('api:create')
TOKEN_URL = reverse('api:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    ''' Test the users API (public) '''

    def set_up(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        ''' Test creating user with valid payload is successful '''
        payload = {
            'email': 'user@email.com',
            'password': 'Password123',
            'name': 'user name'
        }
        res = self.client.post(CREATE_URER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        ''' Test creating user that already exists fails '''
        payload = {
            'email': 'user@email.com',
            'password': 'Password123',
            'name': 'user name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_URER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        ''' Test that the password must be more than 5 characters '''
        payload = {
            'email': 'user@email.com',
            'password': 'P'
        }
        res = self.client.post(CREATE_URER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        ''' Test that a token is created for the user '''
        payload = {
            'email': 'user@email.com', 
            'password': 'Password123',
            'name': 'user name'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        ''' Test that token is not created if invalid credentials are given '''
        create_user(email='user@email.com', password='Password123', name='user name')
        payload = {
            'email': 'user@email.com',
            'password': 'Wrong Password'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        ''' Test that token is not created if user does not exist '''
        payload = {
            'email': 'user@email.com',
            'password': 'Password123'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        ''' Test that email and password are requried '''
        res = self.client.post(TOKEN_URL, {'email': 'user@email.com', 'password': ''})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) 