from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer


class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user, exclude=('id',))
        return Response(serializer.data)
