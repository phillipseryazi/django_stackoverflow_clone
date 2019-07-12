from django.urls import path
from .views import PostQuestionView, UpdateQuestionView, CloseQuestionView

urlpatterns = [
    path('add/', PostQuestionView.as_view(), name='add_question'),
    path('update/<int:id>/', UpdateQuestionView.as_view(), name='update_question'),
    path('close/<int:id>/', CloseQuestionView.as_view(), name='close_question'),
]
