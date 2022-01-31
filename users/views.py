from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser
from users.pagination import CustomPagination
from users.serializers import LoginUserSerializer, BasicUserSerializer, PatchUserSerializer
from utils.serializers import BadRequestSerializer, ValidationErrorSerializer, PaginatedResponceSerializer


class CurrentUserView(APIView):
    def get(self, request):
        serializer = LoginUserSerializer(request.user)
        return Response(serializer.data)


class UsersListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    pagination_class = CustomPagination

    def get_serializer(self, *args, **kwargs):
        serializer = BasicUserSerializer(self.paginate_queryset(self.queryset), many=True)
        return serializer


class UserUpdateView(APIView):
    def patch(self, request, pk):
        get_object_or_404(CustomUser, pk=pk)

        user = request.user
        if user.id == pk:
            serializer = PatchUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)
        else:
            raise ParseError('You cannot change other users data')
