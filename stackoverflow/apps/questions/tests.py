from django.test import TestCase, RequestFactory
from ..users.views import RegistrationView, LoginView
from .views import (PostQuestionView, UpdateQuestionView,
                    CloseQuestionView, UpVoteQuestionView,
                    DownVoteQuestionView, GetRecommendedQuestionsView, SearchQuestionsView)
import json
from minimock import Mock
import smtplib


# Create your tests here.
class QuestionsAppTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        smtplib.SMTP = Mock('smtplib.SMTP')
        smtplib.SMTP.mock_returns = Mock('smtp_connection')
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
        self.update_question = {
            'question': {
                'title': 'updated title',
                'body': 'updated body'
            }
        }
        self.close_question = {
            'question': {
                'is_closed': True
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
        self.user2 = {
            'user': {
                'username': 'test-user2',
                'email': 'test@gmail2.com',
                'bio': 'test-user bio',
                'image': 'https://image.com',
                'password': 'password',
                'isAdmin': True
            }
        }
        self.login_user = {'user': {'email': 'test@gmail.com', 'password': 'password'}}
        self.login_user2 = {'user': {'email': 'test@gmail2.com', 'password': 'password'}}

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

    def test_question_posted(self):
        self.assertEqual(self.qn_result.status_code, 201)

    def test_edit_question(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        request = self.factory.put('/api/v1/questions/update/', **headers, content_type='application/json',
                                   data=json.dumps(self.update_question))
        response = UpdateQuestionView.as_view()(request, **{'id': 1})
        self.assertEqual(response.status_code, 201)

    def test_unauthorized_user_update(self):
        # register user
        self.register(self.user2)
        # login user
        login_response = self.login(self.login_user2)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login_response.data['token']
        }
        request = self.factory.put('/api/v1/questions/update/', **headers, content_type='application/json',
                                   data=json.dumps(self.update_question))
        response = UpdateQuestionView.as_view()(request, **{'id': 1})
        self.assertEqual(response.status_code, 400)

    def test_question_not_found(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        request = self.factory.put('/api/v1/questions/update/', **headers, content_type='application/json',
                                   data=json.dumps(self.update_question))
        response = UpdateQuestionView.as_view()(request, **{'id': 10})
        self.assertEqual(response.status_code, 400)

    def test_close_question(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        request = self.factory.put('/api/v1/questions/close/', **headers, content_type='application/json',
                                   data=json.dumps(self.close_question))
        response = CloseQuestionView.as_view()(request, **{'id': 1})
        self.assertEqual(response.status_code, 201)

    def test_unauthorized_question_close(self):
        # register user
        self.register(self.user2)
        # login user
        login_response = self.login(self.login_user2)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login_response.data['token']
        }
        request = self.factory.put('/api/v1/questions/close/', **headers, content_type='application/json',
                                   data=json.dumps(self.update_question))
        response = CloseQuestionView.as_view()(request, **{'id': 1})
        self.assertEqual(response.status_code, 400)

    def test_close_question_not_found(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        request = self.factory.put('/api/v1/questions/close/', **headers, content_type='application/json',
                                   data=json.dumps(self.update_question))
        response = CloseQuestionView.as_view()(request, **{'id': 10})
        self.assertEqual(response.status_code, 400)

    def test_up_vote_question(self):
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
        # create question
        request = self.factory.post('/api/v1/questions/add/', **headers, content_type='application/json',
                                    data=json.dumps(self.question))
        PostQuestionView.as_view()(request)
        # up vote question
        request = self.factory.post('/api/v1/questions/upvote/', **headers, content_type='application/json',
                                    data=json.dumps(vote))
        response = UpVoteQuestionView.as_view()(request, **{'qid': 1})
        self.assertEqual(response.status_code, 201)

    def test_down_vote_question(self):
        self.register(self.user)
        login_response = self.login(self.login_user)
        vote = {
            'vote': {
                'up_vote': False,
                'down_vote': True
            }
        }
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login_response.data['token']
        }
        # create question
        request = self.factory.post('/api/v1/questions/add/', **headers, content_type='application/json',
                                    data=json.dumps(self.question))
        PostQuestionView.as_view()(request)
        # up vote question
        request = self.factory.post('/api/v1/questions/downvote/', **headers, content_type='application/json',
                                    data=json.dumps(vote))
        response = DownVoteQuestionView.as_view()(request, **{'qid': 1})
        self.assertEqual(response.status_code, 201)

    def test_get_recommendations(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        request = self.factory.get('/api/v1/questions/recommendations/', **headers, content_type='application/json')
        response = GetRecommendedQuestionsView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_search_questions_by_tags(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        request = self.factory.get('/api/v1/questions/search', **headers, content_type='application/json')
        response = SearchQuestionsView.as_view()(request, {'topic': 'django'})
        self.assertEqual(response.status_code, 200)
