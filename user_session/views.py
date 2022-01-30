from django.contrib import auth
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from user_session.serializers import LoginSerializer
from users.serializers import DetailedUserSerializer


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = self.request.data
        login_serializer = LoginSerializer(data=data)

        if login_serializer.is_valid(raise_exception=True):
            email = data['login']
            password = data['password']

            user = auth.authenticate(email=email, password=password)

            if user is not None:
                auth.login(request, user)
                user_serializer = DetailedUserSerializer(user, include_admin=True)
                return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)
            else:
                raise ParseError('Login or password is invalid')


class LogoutView(APIView):
    def post(self, request):
        auth.logout(request)
        return Response(status=status.HTTP_200_OK)
