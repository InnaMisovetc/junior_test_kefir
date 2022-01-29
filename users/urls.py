from django.urls import path

from .views import CurrentUserView, UsersListView, UserUpdateView

urlpatterns = [
    path('', UsersListView.as_view()),
    path('/current', CurrentUserView.as_view()),
    path('/<int:pk>', UserUpdateView.as_view())
]
