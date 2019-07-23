from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (CreateAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .renderers import AnswerRenderer, AnswerListRenderer
from .serializers import PostAnswerSerializer, UpdateAnswerSerializer, VotesSerializer
from .models import Answer, Votes
from ..users.backends import JWTAuthentication
from ...utils.decoder import decode_token
from ...utils.emailer import send_email
from ..questions.models import Question
from ..users.models import User


def get_question(qid):
    return Question.objects.get(id=qid)


def get_user(uid):
    return User.objects.get(id=uid)


# Create your views here.
class PostAnswerView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (AnswerRenderer,)
    serializer_class = PostAnswerSerializer
    lookup_url_kwarg = 'qid'
    email_dict = dict()

    def email(self, request, recipient, payload):
        self.email_dict['sender'] = 'Stackoverflow Clone'
        self.email_dict['recipient'] = recipient
        self.email_dict['subject'] = 'New Answer'
        self.email_dict['type'] = 'Question'
        self.email_dict['content'] = 'Answer'
        self.email_dict['payload'] = payload
        send_email(request=request, data=self.email_dict)

    def post(self, request, *args, **kwargs):
        qid = self.kwargs.get(self.lookup_url_kwarg)
        jwt = JWTAuthentication()
        user = jwt.authenticate(self.request)
        token_data = decode_token(user[1])
        request_data = request.data.get('answer', {})

        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(question_id=qid, user_id=token_data['id'])

        question = get_question(qid)
        user = get_user(question.user_id)
        self.email(request, user.email, question.title)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateAnswerView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (AnswerRenderer,)
    serializer_class = UpdateAnswerSerializer
    lookup_url_kwarg = 'aid'

    def get_queryset(self):
        aid = self.kwargs.get(self.lookup_url_kwarg)
        return Answer.objects.filter(id=aid)

    def update(self, request, *args, **kwargs):
        jwt = JWTAuthentication()
        user = jwt.authenticate(self.request)
        token_data = decode_token(user[1])

        request_data = request.data.get('answer', {})
        queryset = self.get_queryset()

        if not queryset:
            return Response({'details': 'Answer not found'}, status=status.HTTP_400_BAD_REQUEST)

        if not token_data['id'] == queryset[0].user_id:
            return Response({'details': 'You are not authorised to edit this answer.'},
                            status=status.HTTP_400_BAD_REQUEST)

        updated_answer = self.serializer_class().update(queryset[0], request_data)
        return Response(data=self.serializer_class(updated_answer).data, status=status.HTTP_201_CREATED)


def up_badge_user(request, answer):
    user = get_user(answer.user_id)
    email_dict = dict()
    email_dict['sender'] = 'Stackoverflow Clone'
    email_dict['recipient'] = user.email
    email_dict['subject'] = 'New Badge'
    email_dict['type'] = 'Answer'
    email_dict['content'] = 'Upvote'
    email_dict['payload'] = 'You have gained a new badge'
    if answer.up_votes >= 10:
        save_badge(user, request, 'Rookie', email_dict)
    elif answer.up_votes >= 20:
        save_badge(user, request, 'Ranger', email_dict)
    elif answer.up_votes >= 30:
        save_badge(user, request, 'Veteran', email_dict)


def save_badge(user, request, badge, email_dict):
    user.badge = badge
    user.save()
    send_email(request=request, data=email_dict)


class UpVoteAnswerView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (AnswerRenderer,)
    serializer_class = VotesSerializer
    lookup_url_kwarg = 'aid'

    def post(self, request, *args, **kwargs):
        aid = self.kwargs.get(self.lookup_url_kwarg)
        jwt = JWTAuthentication()
        user = jwt.authenticate(self.request)

        request_data = request.data.get('vote', {})
        token_data = decode_token(user[1])

        queryset = Votes.objects.filter(user_id=token_data['id'], answer_id=aid)

        if queryset:
            return Response({'details': 'You already voted on this answer'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=token_data['id'], answer_id=aid)

        answer = Answer.objects.get(id=aid)
        answer.up_votes = answer.up_votes + 1
        answer.save()
        up_badge_user(request, answer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
