from django.urls import path
from .views import PostQuestionView

urlpatterns = [
    path('add/', PostQuestionView.as_view(), name='add_question')
]
