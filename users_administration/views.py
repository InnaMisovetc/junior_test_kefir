from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from users.models import CustomUser
from users.serializers import UserSerializer
from users_administration.pagination import AdminCustomPagination


class PrivateUsersListView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = CustomUser.objects.all()
    pagination_class = AdminCustomPagination

    def get_serializer(self, *args, **kwargs):
        serializer = UserSerializer(self.get_queryset(), fields=('id', 'first_name', 'last_name', 'email'), many=True)
        return serializer
