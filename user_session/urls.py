from django.urls import path, include

from .views import GetCSRFToken


urlpatterns = [
    path('csrf_cookie', GetCSRFToken.as_view()),
]
