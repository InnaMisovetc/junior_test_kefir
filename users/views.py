from django.http import JsonResponse
from rest_framework import generics, status
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


class UserUpdateView(APIView):
    def patch(self, request, pk):
        user = request.user
        if user.id == pk:
            serializer = UserSerializer(user, data=request.data, exclude=('id', 'is_admin'), partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
