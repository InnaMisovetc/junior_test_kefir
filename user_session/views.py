from http.client import responses

from django.contrib import auth
from django.http import JsonResponse
from drf_spectacular.types import OpenApiTypes
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from user_session.serializers import LoginSerializer
from users.serializers import LoginUserSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from utils.serializers import BadRequestSerializer, ValidationErrorSerializer


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(response=LoginUserSerializer, description=responses[200]),
            400: OpenApiResponse(response=BadRequestSerializer, description=responses[400]),
            422: OpenApiResponse(response=ValidationErrorSerializer, description=responses[422])})
    def post(self, request):
        data = self.request.data
        login_serializer = LoginSerializer(data=data)

        if login_serializer.is_valid(raise_exception=True):
            email = data['login']
            password = data['password']

            user = auth.authenticate(email=email, password=password)

            if user is not None:
                auth.login(request, user)
                user_serializer = LoginUserSerializer(user)
                return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)
            else:
                raise ParseError('Login or password is invalid')


class LogoutView(APIView):
    @extend_schema(
        responses={
            200: OpenApiResponse(response=OpenApiTypes.STR, description=responses[200]),
            401: OpenApiResponse(response=OpenApiTypes.STR, description=responses[401])})
    def get(self, request):
        auth.logout(request)
        return Response(status=status.HTTP_200_OK, data='User logged out')
