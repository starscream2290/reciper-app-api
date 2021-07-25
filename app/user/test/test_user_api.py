from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserAPITests(TestCase):
    "Test the users API (public)"

    def setUp(self):
        self.client = APIClient()


    def test_create_valid_user_success(self):
        "Test creating user with valid payload is Succesful"
        payload = {
            'email':'testemail@pldt.com',
            'password':'testpassword',
            'name':'Test Name'
            }
        responce = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**responce.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', responce.data)


    def test_user_exists(self):
        "Test creating a user that already exist fails"
        payload = {'email':'testemail@pldt.com', 'password':'testpassword','name':'Test'}
        create_user(**payload)

        responce = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short(self):
        "Test that the password must be more than 5 char"
        payload = {'email':'testemail@pldt.com.ph', 'password': 'pw', 'name':'Test'}
        responce = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)


    def test_create_token_for_user(self):
        "Test that a token is created for the user"
        payload = {'email':'cris@pldt.com', 'password':'testpw', 'name':'Test Name'}
        create_user (**payload)
        responce = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', responce.data)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        "Test that the token is not created if invalid credetials are given"
        create_user(email='test@pldt.com', password='testpass', name='Test Name')
        payload= {'email':'test@pldt.com', 'password':'wrong','name':'Test Name'}
        responce = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', responce.data)
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        "Test that the token is not created if user doesnt exist"
        payload = {'email':"test@pldt.com", 'password':'testpass', 'name':'Test Name'}
        responce = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', responce.data)
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        "Test that email and password are required"
        responce = self.client.post(TOKEN_URL, {'email':'myemail','password':''})

        self.assertNotIn('token', responce.data)
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
