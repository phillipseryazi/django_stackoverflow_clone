from django.test import TestCase, RequestFactory
from ..users.views import RegistrationView, LoginView
from .views import PostAnswerView, UpdateAnswerView, UpVoteAnswerView
from ..questions.views import PostQuestionView

import json
from minimock import Mock
import smtplib


# Create your tests here.
class AnswersAppTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        smtplib.SMTP = Mock('smtplib.SMTP')
        smtplib.SMTP.mock_returns = Mock('smtp_connection')
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
        self.user2 = {
            'user': {
                'username': 'test-user2',
                'email': 'test2@gmail.com',
                'bio': 'test-user bio',
                'image': 'https://image.com',
                'password': 'password',
                'isAdmin': True
            }
        }
        self.login_user = {'user': {'email': 'test@gmail.com', 'password': 'password'}}
        self.login_user2 = {'user': {'email': 'test2@gmail.com', 'password': 'password'}}

        # questions and answers
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
        self.answer = {
            'answer': {
                'body': 'this is an answer'
            }
        }
        self.update_answer = {
            'answer': {
                'body': 'this is the answer update'
            }
        }

        # register user
        self.register(self.user)

        # login user
        self.login_response = self.login(self.login_user)

        # create question
        self.qn_result = self.create_question()

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

    def create_question(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        request = self.factory.post('/api/v1/questions/add/', **headers, content_type='application/json',
                                    data=json.dumps(self.question))
        response = PostQuestionView.as_view()(request)
        return response

    def test_answer_question(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        request = self.factory.post('/api/v1/questions/answers/add/', **headers, content_type='application/json',
                                    data=json.dumps(self.answer))
        response = PostAnswerView.as_view()(request, **{'qid': 1})
        self.assertEqual(response.status_code, 201)

    def test_answer_update(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        # answer question
        request = self.factory.post('/api/v1/questions/answers/add/', **headers, content_type='application/json',
                                    data=json.dumps(self.answer))
        PostAnswerView.as_view()(request, **{'qid': 1})
        # update answer
        request = self.factory.put('/api/v1/questions/answers/update/', **headers, content_type='application/json',
                                   data=json.dumps(self.update_answer))
        response = UpdateAnswerView.as_view()(request, **{'aid': 1})
        self.assertEqual(response.status_code, 201)

    def test_update_unknown_answer(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        request = self.factory.put('/api/v1/questions/answers/update/', **headers, content_type='application/json',
                                   data=json.dumps(self.update_answer))
        response = UpdateAnswerView.as_view()(request, **{'aid': 2})
        self.assertEqual(response.status_code, 400)

    def test_unauthorized_answer_update(self):
        self.register(self.user2)
        login_response = self.login(self.login_user2)
        self.create_question()
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        # answer question
        request = self.factory.post('/api/v1/questions/answers/add/', **headers, content_type='application/json',
                                    data=json.dumps(self.answer))
        PostAnswerView.as_view()(request, **{'qid': 1})
        headers2 = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login_response.data['token']
        }
        # update answer
        request = self.factory.put('/api/v1/questions/answers/update/', **headers2, content_type='application/json',
                                   data=json.dumps(self.update_answer))
        response = UpdateAnswerView.as_view()(request, **{'aid': 1})
        self.assertEqual(response.status_code, 400)

    def test_up_vote_answer(self):
        self.register(self.user)
        login_response = self.login(self.login_user)
        vote = {
            'vote': {
                'up_vote': True,
                'down_vote': False
            }
        }
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login_response.data['token']
        }
        request = self.factory.post('/api/v1/questions/answers/add/', **headers, content_type='application/json',
                                    data=json.dumps(self.answer))
        PostAnswerView.as_view()(request, **{'qid': 1})
        # up vote answer
        request2 = self.factory.post('/api/v1/questions/answers/upvote/', **headers, content_type='application/json',
                                     data=json.dumps(vote))
        response = UpVoteAnswerView.as_view()(request2, **{'aid': 1})
        self.assertEqual(response.status_code, 201)

    def test_double_up_vote_answer(self):
        self.register(self.user)
        login_response = self.login(self.login_user)
        vote = {
            'vote': {
                'up_vote': True,
                'down_vote': False
            }
        }
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login_response.data['token']
        }
        request = self.factory.post('/api/v1/questions/answers/add/', **headers, content_type='application/json',
                                    data=json.dumps(self.answer))
        PostAnswerView.as_view()(request, **{'qid': 1})
        # up vote answer
        request2 = self.factory.post('/api/v1/questions/answers/upvote/', **headers, content_type='application/json',
                                     data=json.dumps(vote))
        UpVoteAnswerView.as_view()(request2, **{'aid': 1})
        # up vote same answer again
        request3 = self.factory.post('/api/v1/questions/answers/upvote/', **headers, content_type='application/json',
                                     data=json.dumps(vote))
        response = UpVoteAnswerView.as_view()(request3, **{'aid': 1})
        self.assertEqual(response.status_code, 400)
