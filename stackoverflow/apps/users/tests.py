import json
import os
from datetime import timedelta, datetime

import jwt
from django.test import TestCase, RequestFactory

from .backends import JWTAuthentication
from .views import RegistrationView, LoginView, UserProfileView


# Create your tests here.


class UsersAppTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.auth = JWTAuthentication()
        self.reg_user = {'user':
            {
                'username': 'test-user',
                'email': 'test@gmail.com',
                'bio': 'test-user bio',
                'image': 'https://image.com',
                'password': 'password',
                'isAdmin': True
            }
        }

        self.reg_user2 = {'user':
            {
                'username': 'test-user',
                'email': 'test@gmail.com',
                'bio': 'test-user bio',
                'image': 'https://image.com',
                'password': 'passwo',
                'isAdmin': True
            }
        }

        self.login_user = {'user': {'email': 'test@gmail.com', 'password': 'password'}}
        self.login_user2 = {'user': {'email': 'xxx@gmail.com', 'password': 'password'}}

    def register(self, user):
        request = self.factory.post('/api/v1/auth/signup/',
                                    data=json.dumps(user),
                                    content_type='application/json')
        response = RegistrationView.as_view()(request)
        return response

    def login(self, user):
        request = self.factory.post('/api/v1/auth/login/',
                                    data=json.dumps(user),
                                    content_type='application/json')
        response = LoginView.as_view()(request)
        return response

    def test_user_registration_success(self):
        response = self.register(self.reg_user)
        self.assertEqual(response.status_code, 201)

    def test_user_reg_short_password(self):
        response = self.register(self.reg_user2)
        self.assertEqual(response.status_code, 400)

    def test_user_login_success(self):
        # register the user
        self.register(self.reg_user)
        # login the user
        response = self.login(self.login_user)
        self.assertEqual(response.status_code, 200)

    def test_user_login_fail(self):
        # register the user
        self.register(self.reg_user)
        # login the user
        response = self.login(self.login_user2)
        self.assertEqual(response.status_code, 400)

    def test_no_auth_header(self):
        request = self.factory.post('/api/v1/auth/signup/', content_type='application/json',
                                    data=json.dumps(self.reg_user))
        response = self.auth.authenticate(request)
        self.assertEquals(None, response)

    def test_auth_header_length_less_than_one(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token '
        }
        request = self.factory.post('/api/v1/auth/signup/', **headers, content_type='application/json',
                                    data=json.dumps(self.reg_user))
        response = self.auth.authenticate(request)
        self.assertEquals(None, response)

    def test_auth_header_length_greater_than_two(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token Bearer Token'
        }
        request = self.factory.post('/api/v1/auth/signup/', **headers, content_type='application/json',
                                    data=json.dumps(self.reg_user))
        response = self.auth.authenticate(request)
        self.assertEquals(None, response)

    def test_token_prefix_validity(self):
        self.register(self.reg_user)
        login_response = self.login(self.login_user)
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + login_response.data['token']
        }
        request = self.factory.post('/api/v1/auth/signup/', **headers, content_type='application/json',
                                    data=json.dumps(self.reg_user))
        response = self.auth.authenticate(request)
        self.assertEquals(None, response)

    def test_invalid_token(self):
        request = ''
        with self.assertRaises(Exception) as context:
            self.auth._authenticate_credentials(request, 'this_is_not_a_token')
        self.assertIn('Authentication failed!', str(context.exception))

    def test_user_not_recognised(self):
        # create token
        dt = datetime.now() + timedelta(days=1)
        token = jwt.encode({
            'id': 2,
            'exp': int(dt.strftime('%s')),
            'username': self.reg_user['user']['username'],
            'email': self.reg_user['user']['email']
        }, os.environ['APP_SECRET'], algorithm='HS256')
        # create request
        request = ''
        # assert exception
        with self.assertRaises(Exception) as context:
            self.auth._authenticate_credentials(request, token)
        self.assertIn('User not recognised.', str(context.exception))

    def test_credentials_validity_success(self):
        # register user
        self.register(self.reg_user)
        # login user
        login_response = self.login(self.login_user)
        # create a dummy request
        request = ''
        # call target method
        result = self.auth._authenticate_credentials(request, login_response.data['token'])
        # assert
        self.assertEquals(self.reg_user['user']['email'], str(result[0]))

    def test_get_user_profile(self):
        # register user
        self.register(self.reg_user)
        # login user
        login_response = self.login(self.login_user)
        # get user profile
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login_response.data['token']
        }
        request = self.factory.get('/api/v1/auth/profile/', **headers, content_type='application/json')
        response = UserProfileView.as_view()(request)
        self.assertEqual(response.status_code, 200)


