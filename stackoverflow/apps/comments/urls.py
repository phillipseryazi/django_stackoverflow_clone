from django.urls import path
from .views import (PostQuestionCommentView, UpdateQuestionCommentView,
                    DeleteQuestionComment, PostAnswerCommentView, UpdateAnswerCommentView)

urlpatterns = [
    path('add/<int:qid>/', PostQuestionCommentView.as_view(), name='add_question_comment'),
    path('update/<int:cid>/', UpdateQuestionCommentView.as_view(), name='update_question_comment'),
    path('delete/<int:cid>/', DeleteQuestionComment.as_view(), name='delete_question_comment'),
    path('answers/add/<int:aid>/', PostAnswerCommentView.as_view(), name='add_answer_comment'),
    path('answers/update/<int:cid>/', UpdateAnswerCommentView.as_view(), name='update_answer_comment'),
]
