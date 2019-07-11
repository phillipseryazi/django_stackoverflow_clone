from rest_framework.generics import (CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .renderers import QuestionRenderer
from .serializers import PostQuestionSerializer
from ..users.backends import JWTAuthentication
from ...utils.decoder import decode_token
from .models import Tag


def save_tags(qn_id, request_data):
    for item in request_data['tags']:
        tag = Tag(question=qn_id, tag=item)
        tag.save()


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
