from django.urls import path
from .views import PrivateUsersListView


urlpatterns = [
    path('', PrivateUsersListView.as_view()),
]
