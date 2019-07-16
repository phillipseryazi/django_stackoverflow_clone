from django.urls import path
from .views import PostAnswerView, UpdateAnswerView

urlpatterns = [
    path('add/<int:qid>/', PostAnswerView.as_view(), name='add_answer'),
    path('update/<int:aid>/', UpdateAnswerView.as_view(), name='update_answer'),
]
