from rest_framework.generics import (CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions

from .renderers import QuestionRenderer
from .serializers import PostQuestionSerializer, UpdateQuestionSerializer
from ..users.backends import JWTAuthentication
from ...utils.decoder import decode_token
from .models import Tag, Question


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
            return Response({'details': 'Item not found'}, status=status.HTTP_400_BAD_REQUEST)

        if not token_data['id'] == queryset[0].user_id:
            return Response({'details': 'You are not authorised to edit this item.'},
                            status=status.HTTP_400_BAD_REQUEST)

        updated_property = self.serializer_class().update(queryset[0], request_data)
        return Response(data=self.serializer_class(updated_property).data, status=status.HTTP_201_CREATED)
