from rest_framework.generics import (CreateAPIView, UpdateAPIView, DestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .renderers import CommentRenderer, CommentListRenderer
from .serializers import (PostQuestionCommentSerializer, UpdateQuestionCommentSerializer,
                          PostAnswerCommentSerializer, UpdateAnswerCommentSerializer)
from ..users.backends import JWTAuthentication
from ...utils.decoder import decode_token
from ...utils.emailer import send_email
from .models import QuestionComment, AnswerComment
from ..questions.models import Question
from ..users.models import User


def get_question(qid):
    return Question.objects.get(id=qid)


def get_user(uid):
    return User.objects.get(id=uid)


class PostQuestionCommentView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CommentRenderer,)
    serializer_class = PostQuestionCommentSerializer
    lookup_url_kwarg = 'qid'
    email_dict = dict()

    def email(self, request, recipient, payload):
        self.email_dict['sender'] = 'Stackoverflow Clone'
        self.email_dict['recipient'] = recipient
        self.email_dict['subject'] = 'New Comment'
        self.email_dict['type'] = 'Question'
        self.email_dict['content'] = 'Comment'
        self.email_dict['payload'] = payload
        send_email(request=request, data=self.email_dict)

    def post(self, request, *args, **kwargs):
        qid = self.kwargs.get(self.lookup_url_kwarg)
        jwt = JWTAuthentication()
        user = jwt.authenticate(self.request)
        token_data = decode_token(user[1])
        request_data = request.data.get('comment', {})

        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(question_id=qid, user_id=token_data['id'])

        question = get_question(qid)
        user = get_user(question.user_id)
        self.email(request, user.email, question.title)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateQuestionCommentView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CommentRenderer,)
    serializer_class = UpdateQuestionCommentSerializer
    lookup_url_kwarg = 'cid'

    def get_queryset(self):
        cid = self.kwargs.get(self.lookup_url_kwarg)
        return QuestionComment.objects.filter(id=cid)

    def put(self, request, *args, **kwargs):
        jwt = JWTAuthentication()
        user = jwt.authenticate(self.request)
        token_data = decode_token(user[1])

        request_data = request.data.get('comment', {})
        queryset = self.get_queryset()

        if not queryset:
            return Response({'details': 'Comment not found'}, status=status.HTTP_400_BAD_REQUEST)

        if not token_data['id'] == queryset[0].user_id:
            return Response({'details': 'You are not authorised to edit this question.'},
                            status=status.HTTP_400_BAD_REQUEST)

        updated_comment = self.serializer_class().update(queryset[0], request_data)
        return Response(data=self.serializer_class(updated_comment).data, status=status.HTTP_201_CREATED)


class DeleteQuestionComment(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'cid'

    def get_queryset(self):
        cid = self.kwargs.get(self.lookup_url_kwarg)
        return QuestionComment.objects.filter(id=cid)

    def delete(self, request, *args, **kwargs):
        jwt = JWTAuthentication()
        user = jwt.authenticate(self.request)
        token_data = decode_token(user[1])

        queryset = self.get_queryset()

        if not queryset:
            return Response({'details': 'No such comment was found.'}, status=status.HTTP_404_NOT_FOUND)

        if not token_data['id'] == queryset[0].user_id:
            return Response({'details': 'You are not authorised to delete this item.'},
                            status=status.HTTP_400_BAD_REQUEST)

        queryset.delete()
        return Response({'details': 'Comment was deleted.'}, status=status.HTTP_200_OK)


class PostAnswerCommentView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CommentRenderer,)
    serializer_class = PostAnswerCommentSerializer
    lookup_url_kwarg = 'aid'

    def post(self, request, *args, **kwargs):
        aid = self.kwargs.get(self.lookup_url_kwarg)
        jwt = JWTAuthentication()
        user = jwt.authenticate(self.request)
        token_data = decode_token(user[1])
        request_data = request.data.get('comment', {})
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(answer_id=aid, user_id=token_data['id'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateAnswerCommentView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CommentRenderer,)
    serializer_class = UpdateAnswerCommentSerializer
    lookup_url_kwarg = 'cid'

    def get_queryset(self):
        cid = self.kwargs.get(self.lookup_url_kwarg)
        return AnswerComment.objects.filter(id=cid)

    def put(self, request, *args, **kwargs):
        jwt = JWTAuthentication()
        user = jwt.authenticate(self.request)
        token_data = decode_token(user[1])

        request_data = request.data.get('comment', {})
        queryset = self.get_queryset()

        if not queryset:
            return Response({'details': 'Comment not found'}, status=status.HTTP_400_BAD_REQUEST)

        if not token_data['id'] == queryset[0].user_id:
            return Response({'details': 'You are not authorised to edit this question.'},
                            status=status.HTTP_400_BAD_REQUEST)

        updated_comment = self.serializer_class().update(queryset[0], request_data)
        return Response(data=self.serializer_class(updated_comment).data, status=status.HTTP_201_CREATED)
