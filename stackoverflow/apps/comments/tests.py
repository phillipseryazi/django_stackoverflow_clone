from datetime import datetime, timedelta

from django.test import TestCase, RequestFactory
from ..users.views import RegistrationView, LoginView
from ..questions.views import PostQuestionView
from .views import (PostQuestionCommentView, UpdateQuestionCommentView,
                    DeleteQuestionComment, PostAnswerCommentView,
                    UpdateAnswerCommentView)
from ..answers.views import PostAnswerView

import json
from minimock import Mock
import smtplib


# Create your tests here.
class CommentsAppTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        smtplib.SMTP = Mock('smtplib.SMTP')
        smtplib.SMTP.mock_returns = Mock('smtp_connection')
        # user credentials
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

        # questions and comments
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
        self.question_comment = {
            'comment': {
                'comment': 'adding a comment'
            }
        }
        self.update_qn_comment = {
            'comment': {
                'comment': 'updating a comment'
            }
        }

        self.answer = {
            'answer': {
                'body': 'this is an answer'
            }
        }

        # register user
        self.register(self.user)

        # login user
        self.login_response = self.login(self.login_user)

        # create question
        self.qn_result = self.create_question()

        # create answer
        self.ans_result = self.create_answer()

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

    def create_answer(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        request = self.factory.post('/api/v1/questions/answers/add/', **headers, content_type='application/json',
                                    data=json.dumps(self.answer))
        response = PostAnswerView.as_view()(request, **{'qid': 1})
        return response

    def add_question_comment(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        request = self.factory.post('/api/v1/questions/comments/add/', **headers, content_type='application/json',
                                    data=json.dumps(self.question_comment))
        response = PostQuestionCommentView.as_view()(request, **{'qid': 1})
        return response

    def update_question_comment(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        request = self.factory.put('/api/v1/questions/comments/update/', **headers, content_type='application/json',
                                   data=json.dumps(self.update_qn_comment))
        response = UpdateQuestionCommentView.as_view()(request, **{'cid': 1})
        return response

    def delete_question_comment(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        request = self.factory.delete('/api/v1/questions/comments/delete/', **headers, content_type='application/json')
        response = DeleteQuestionComment.as_view()(request, **{'cid': 1})
        return response

    def test_post_question_comment(self):
        response = self.add_question_comment()
        self.assertEqual(response.status_code, 201)

    def test_update_question_comment(self):
        self.add_question_comment()
        response = self.update_question_comment()
        self.assertEqual(response.status_code, 201)

    def test_unauthorized_update_qn_comment(self):
        self.register(self.user2)
        login_response = self.login(self.login_user2)
        self.create_question()
        self.add_question_comment()
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login_response.data['token']
        }
        request = self.factory.put('/api/v1/questions/comments/update/', **headers, content_type='application/json',
                                   data=json.dumps(self.update_qn_comment))
        response = UpdateQuestionCommentView.as_view()(request, **{'cid': 1})
        self.assertEqual(response.status_code, 400)

    def test_update_question_comment_not_found(self):
        response = self.update_question_comment()
        self.assertEqual(response.status_code, 400)

    def test_unauthorized_delete_qn_comment(self):
        self.register(self.user2)
        login_response = self.login(self.login_user2)
        self.create_question()
        self.add_question_comment()
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login_response.data['token']
        }
        request = self.factory.delete('/api/v1/questions/comments/delete/', **headers, content_type='application/json')
        response = DeleteQuestionComment.as_view()(request, **{'cid': 1})
        self.assertEqual(response.status_code, 400)

    def test_delete_question_comment(self):
        self.add_question_comment()
        response = self.delete_question_comment()
        self.assertEqual(response.status_code, 200)

    def test_delete_question_comment_not_found(self):
        response = self.delete_question_comment()
        self.assertEqual(response.status_code, 404)

    def add_answer_comment(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        request = self.factory.post('/api/v1/questions/comments/answers/add/', **headers,
                                    content_type='application/json',
                                    data=json.dumps(self.question_comment))
        response = PostAnswerCommentView.as_view()(request, **{'aid': 1})
        return response

    def update_answer_comment(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login_response.data['token']
        }
        request = self.factory.put('/api/v1/questions/comments/answers/add/', **headers,
                                   content_type='application/json',
                                   data=json.dumps(self.update_qn_comment))
        response = UpdateAnswerCommentView.as_view()(request, **{'cid': 1})
        return response

    def test_post_answer_comment(self):
        response = self.add_answer_comment()
        self.assertEqual(response.status_code, 201)

    def test_update_answer_comment(self):
        self.add_answer_comment()
        response = self.update_answer_comment()
        self.assertEqual(response.status_code, 201)

    def test_unauthorized_update_ans_comment(self):
        self.register(self.user2)
        login_response = self.login(self.login_user2)
        self.create_answer()
        self.add_answer_comment()
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login_response.data['token']
        }
        request = self.factory.put('/api/v1/questions/comments/answers/add/', **headers,
                                   content_type='application/json',
                                   data=json.dumps(self.update_qn_comment))
        response = UpdateAnswerCommentView.as_view()(request, **{'cid': 1})
        self.assertEqual(response.status_code, 400)

    def test_update_ans_comment_not_found(self):
        response = self.update_answer_comment()
        self.assertEqual(response.status_code, 400)
