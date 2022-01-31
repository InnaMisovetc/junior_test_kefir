from http.client import responses

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics, status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser
from users.pagination import CustomPagination
from users.serializers import LoginUserSerializer, BasicUserSerializer, PatchUserSerializer
from utils.serializers import BadRequestSerializer, ValidationErrorSerializer, PaginatedResponceSerializer


class CurrentUserView(APIView):

    @extend_schema(
        responses={
            200: OpenApiResponse(response=LoginUserSerializer, description=responses[200]),
            401: OpenApiResponse(response=OpenApiTypes.STR, description=responses[200])})
    def get(self, request):
        serializer = LoginUserSerializer(request.user)
        return Response(serializer.data)


@method_decorator(
    name='get',
    decorator=extend_schema(
        responses={
            200: OpenApiResponse(response=PaginatedResponceSerializer, description=responses[200]),
            400: OpenApiResponse(response=BadRequestSerializer, description=responses[400]),
            401: OpenApiResponse(response=OpenApiTypes.STR, description=responses[401]),
            422: OpenApiResponse(response=ValidationErrorSerializer, description=responses[422])}))
class UsersListView(generics.ListAPIView):
    queryset = CustomUser.objects.all().order_by('id')
    pagination_class = CustomPagination

    def get_serializer(self, *args, **kwargs):
        serializer = BasicUserSerializer(self.paginate_queryset(self.queryset), many=True)
        return serializer


class UserUpdateView(APIView):
    @extend_schema(
        request=PatchUserSerializer,
        responses={
            200: OpenApiResponse(response=PatchUserSerializer, description=responses[200]),
            400: OpenApiResponse(response=BadRequestSerializer, description=responses[400]),
            401: OpenApiResponse(response=OpenApiTypes.STR, description=responses[401]),
            404: OpenApiResponse(response=OpenApiTypes.STR, description=responses[404]),
            422: OpenApiResponse(response=ValidationErrorSerializer, description=responses[422])})
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
