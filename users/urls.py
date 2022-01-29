from django.urls import path

from .views import CurrentUserView, UsersListView

urlpatterns = [
    path('', UsersListView.as_view()),
    path('/current', CurrentUserView.as_view()),
]
