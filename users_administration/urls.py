from django.urls import path
from .views import PrivateUsersListCreateView, PrivateUserRetrieveUpdateDestroyView


urlpatterns = [
    path('', PrivateUsersListCreateView.as_view()),
    path('/<int:pk>', PrivateUserRetrieveUpdateDestroyView.as_view())
]
