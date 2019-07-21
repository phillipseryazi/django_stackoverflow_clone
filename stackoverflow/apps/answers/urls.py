from django.urls import path
from .views import PostAnswerView, UpdateAnswerView, UpVoteAnswerView

urlpatterns = [
    path('add/<int:qid>/', PostAnswerView.as_view(), name='add_answer'),
    path('update/<int:aid>/', UpdateAnswerView.as_view(), name='update_answer'),
    path('upvote/<int:aid>/', UpVoteAnswerView.as_view(), name='up_vote_answer'),
]
