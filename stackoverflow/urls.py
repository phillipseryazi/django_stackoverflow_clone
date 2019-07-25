"""stackoverflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Stackoverflow Clone',
        default_version='v1',
        description='A clone of the popular question-answer site stackoverflow.',
        contact=openapi.Contact(email='phillip.seryazi@andela.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/auth/', include('stackoverflow.apps.users.urls')),
    path('api/v1/questions/', include('stackoverflow.apps.questions.urls')),
    path('api/v1/questions/comments/', include('stackoverflow.apps.comments.urls')),
    path('api/v1/questions/answers/', include('stackoverflow.apps.answers.urls'))
]
