from django.urls import path
from .views import PostQuestionView, UpdateQuestionView

urlpatterns = [
    path('add/', PostQuestionView.as_view(), name='add_question'),
    path('update/<int:id>/', UpdateQuestionView.as_view(), name='update_question'),
]
