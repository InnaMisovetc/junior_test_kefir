from django.urls import path

from .views import GetCSRFToken, LoginView


urlpatterns = [
    path('csrf_cookie', GetCSRFToken.as_view()),
    path('login', LoginView.as_view())
]
