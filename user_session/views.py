from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib import auth
from django.http import JsonResponse

from user_session.serializers import LoginSerializer
from users.serializers import UserSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response({'success': 'CSRF cookie set'})


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
                user_serializer = UserSerializer(user, exclude=('id',))
                return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'code': 400, 'message': 'Invalid login or password'})
