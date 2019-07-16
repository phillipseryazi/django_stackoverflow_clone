from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (CreateAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .renderers import AnswerRenderer, AnswerListRenderer
from .serializers import PostAnswerSerializer, UpdateAnswerSerializer
from .models import Answer
from ..users.backends import JWTAuthentication
from ...utils.decoder import decode_token


# Create your views here.
class PostAnswerView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (AnswerRenderer,)
    serializer_class = PostAnswerSerializer
    lookup_url_kwarg = 'qid'

    def post(self, request, *args, **kwargs):
        qid = self.kwargs.get(self.lookup_url_kwarg)
        jwt = JWTAuthentication()
        user = jwt.authenticate(self.request)
        token_data = decode_token(user[1])
        request_data = request.data.get('answer', {})
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(question_id=qid, user_id=token_data['id'])
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
