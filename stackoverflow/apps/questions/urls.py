from django.urls import path
from .views import (PostQuestionView, UpdateQuestionView, CloseQuestionView, UpVoteQuestionView, DownVoteQuestion)

urlpatterns = [
    path('add/', PostQuestionView.as_view(), name='add_question'),
    path('update/<int:id>/', UpdateQuestionView.as_view(), name='update_question'),
    path('close/<int:id>/', CloseQuestionView.as_view(), name='close_question'),
    path('upvote/', UpVoteQuestionView.as_view(), name='up_vote_question'),
    path('downvote/', DownVoteQuestion.as_view(), name='down_vote_question'),
]
