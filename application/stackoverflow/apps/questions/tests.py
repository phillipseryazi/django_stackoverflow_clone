from django.test import TestCase, RequestFactory
from ..users.views import RegistrationView, LoginView
from .views import PostQuestionView
import json


# Create your tests here.
class QuestionsAppTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.question = {
            "question": {
                "title": "sample title",
                "body": "sample body.",
                "is_open": True,
                "is_resolved": False,
                "is_closed": False,
                "tags": ["python", "django"]
            }
        }
        self.user = {
            'user': {
                'username': 'test-user',
                'email': 'test@gmail.com',
                'bio': 'test-user bio',
                'image': 'https://image.com',
                'password': 'password',
                'isAdmin': True
            }
        }
        self.login_user = {'user': {'email': 'test@gmail.com', 'password': 'password'}}

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

    def test_question_posted(self):
        # register user
        self.register(self.user)
        # login user and get token
        login_response = self.login(self.login_user)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login_response.data['token']
        }
        request = self.factory.post('/api/v1/questions/add/', **headers, content_type='application/json',
                                    data=json.dumps(self.question))
        response = PostQuestionView.as_view()(request)
        self.assertEqual(response.status_code, 201)
