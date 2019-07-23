from django.urls import path
from .views import (PostQuestionView, UpdateQuestionView,
                    CloseQuestionView, UpVoteQuestionView, DownVoteQuestionView,
                    GetRecommendedQuestionsView, SearchQuestionsView, )

urlpatterns = [
    path('add/', PostQuestionView.as_view(), name='add_question'),
    path('update/<int:id>/', UpdateQuestionView.as_view(), name='update_question'),
    path('close/<int:id>/', CloseQuestionView.as_view(), name='close_question'),
    path('upvote/<int:qid>/', UpVoteQuestionView.as_view(), name='up_vote_question'),
    path('downvote/<int:qid>/', DownVoteQuestionView.as_view(), name='down_vote_question'),
    path('recommendations/', GetRecommendedQuestionsView.as_view(), name='get_recommended_questions'),
    path('search/', SearchQuestionsView.as_view(), name='search_questions'),
]
