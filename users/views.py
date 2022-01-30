from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser
from users.pagination import CustomPagination
from users.serializers import BasicUserSerializer, DetailedUserSerializer


class CurrentUserView(APIView):
    def get(self, request):
        serializer = DetailedUserSerializer(request.user, include_admin=True)
        return Response(serializer.data)


class UsersListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    pagination_class = CustomPagination

    def get_serializer(self, *args, **kwargs):
        serializer = BasicUserSerializer(self.get_queryset(), include_id=True, many=True)
        return serializer


class UserUpdateView(APIView):
    def patch(self, request, pk):
        get_object_or_404(CustomUser, pk=pk)

        user = request.user
        if user.id == pk:
            serializer = DetailedUserSerializer(user, data=request.data, include_id=True, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)
        else:
            raise ParseError('You cannot change other users data')
