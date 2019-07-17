from django.urls import path, include
from .views import (RegistrationView, LoginView, LogoutView, UserProfileView)

urlpatterns = [
    path('signup/', RegistrationView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
