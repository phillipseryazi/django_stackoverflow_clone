from rest_framework.generics import (CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from .renderers import (QuestionRenderer, VotesRenderer, QuestionListRenderer)
from .serializers import (PostQuestionSerializer, UpdateQuestionSerializer,
                          CloseQuestionSerializer, VotesSerializer, GetQuestionSerializer)
from ..users.backends import JWTAuthentication
from ...utils.decoder import decode_token
from .models import Tag, Question, Votes
from ..users.models import User
from ...utils.emailer import send_email


def save_tags(qn_id, request_data):
    for item in request_data['tags']:
        tag = Tag(question=qn_id, tag=item)
        tag.save()


def get_question(qid):
    return Question.objects.get(id=qid)


def get_user(uid):
    return User.objects.get(id=uid)


class PostQuestionView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (QuestionRenderer,)
    serializer_class = PostQuestionSerializer

    def post(self, request, *args, **kwargs):
        jwt = JWTAuthentication()
        user = jwt.authenticate(self.request)
        token_data = decode_token(user[1])
        request_data = request.data.get('question', {})
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        qn_id = serializer.save(slug=serializer.get_slug(request_data.get('title')), user_id=token_data['id'])
        save_tags(qn_id, request_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateQuestionView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (QuestionRenderer,)
    serializer_class = UpdateQuestionSerializer
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        qn_id = self.kwargs.get(self.lookup_url_kwarg)
        return Question.objects.filter(id=qn_id)

    def put(self, request, *args, **kwargs):
        jwt = JWTAuthentication()
        user = jwt.authenticate(self.request)
        token_data = decode_token(user[1])

        request_data = request.data.get('question', {})
        queryset = self.get_queryset()

        if not queryset:
            return Response({'details': 'Question not found'}, status=status.HTTP_400_BAD_REQUEST)

        if not token_data['id'] == queryset[0].user_id:
            return Response({'details': 'You are not authorised to edit this question.'},
                            status=status.HTTP_400_BAD_REQUEST)

        updated_question = self.serializer_class().update(queryset[0], request_data)
        return Response(data=self.serializer_class(updated_question).data, status=status.HTTP_201_CREATED)


class CloseQuestionView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (QuestionRenderer,)
    serializer_class = CloseQuestionSerializer
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        qn_id = self.kwargs.get(self.lookup_url_kwarg)
        return Question.objects.filter(id=qn_id)

    def put(self, request, *args, **kwargs):
        jwt = JWTAuthentication()
        user = jwt.authenticate(self.request)
        token_data = decode_token(user[1])

        request_data = request.data.get('question', {})
        queryset = self.get_queryset()

        if not queryset:
            return Response({'details': 'Question not found'}, status=status.HTTP_400_BAD_REQUEST)

        if not token_data['id'] == queryset[0].user_id:
            return Response({'details': 'You are not authorised to edit this question'},
                            status=status.HTTP_400_BAD_REQUEST)

        updated_property = self.serializer_class().update(queryset[0], request_data)
        return Response(data=self.serializer_class(updated_property).data, status=status.HTTP_201_CREATED)


class UpVoteQuestionView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (VotesRenderer,)
    serializer_class = VotesSerializer
    lookup_url_kwarg = 'qid'
    email_dict = dict()

    def email(self, request, recipient, payload):
        self.email_dict['sender'] = 'Stackoverflow Clone'
        self.email_dict['recipient'] = recipient
        self.email_dict['subject'] = 'New Upvote'
        self.email_dict['type'] = 'Question'
        self.email_dict['content'] = 'Upvote'
        self.email_dict['payload'] = payload
        send_email(request=request, data=self.email_dict)

    def post(self, request, *args, **kwargs):
        qid = self.kwargs.get(self.lookup_url_kwarg)
        jwt = JWTAuthentication()
        user = jwt.authenticate(self.request)

        request_data = request.data.get('vote', {})
        token_data = decode_token(user[1])

        queryset = Votes.objects.filter(user_id=token_data['id'], question_id=qid)

        if queryset:
            return Response({'details': 'You already voted on this question'}, status=status.HTTP_200_OK)

        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=token_data['id'], question_id=qid)

        question = get_question(qid)
        user = get_user(question.user_id)
        self.email(request, user.email, question.title)

        question = Question.objects.get(id=qid)
        question.up_votes = question.up_votes + 1
        question.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DownVoteQuestionView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (VotesRenderer,)
    serializer_class = VotesSerializer
    lookup_url_kwarg = 'qid'

    def post(self, request, *args, **kwargs):
        qid = self.kwargs.get(self.lookup_url_kwarg)
        jwt = JWTAuthentication()
        user = jwt.authenticate(self.request)

        request_data = request.data.get('vote', {})
        token_data = decode_token(user[1])

        queryset = Votes.objects.filter(user_id=token_data['id'], question_id=qid)
        if queryset:
            return Response({'details': 'You already voted on this question'}, status=status.HTTP_200_OK)

        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=token_data['id'], question_id=qid)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetRecommendedQuestionsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (QuestionListRenderer,)
    serializer_class = GetQuestionSerializer

    def get_queryset(self):
        return Question.objects.all().filter().order_by('up_votes')


class SearchQuestionsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (QuestionListRenderer,)
    serializer_class = GetQuestionSerializer

    def get_queryset(self):
        param = self.request.query_params.get('topic', '')
        return Question.objects.all().filter(question_tag_fk__tag=param).order_by('id')
