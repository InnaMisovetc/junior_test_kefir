from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser
from users.pagination import CustomPagination
from users.serializers import UserSerializer


class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user, exclude=('id',))
        return Response(serializer.data)


class UsersListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    pagination_class = CustomPagination

    def get_serializer(self, *args, **kwargs):
        serializer = UserSerializer(self.get_queryset(), fields=('id', 'first_name', 'last_name', 'email'), many=True)
        return serializer
