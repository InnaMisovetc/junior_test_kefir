from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser
from users.serializers import BasicUserSerializer, PrivateUserSerializer, UpdatePrivateUserSerializer
from users_administration.pagination import AdminCustomPagination
from .permissions import AdministrationPermission


class PrivateUsersListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, AdministrationPermission)
    queryset = CustomUser.objects.all()
    pagination_class = AdminCustomPagination

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'GET':
            serializer = BasicUserSerializer(self.get_queryset(), include_id=True,
                                             many=True)
        else:
            serializer = PrivateUserSerializer(data=self.request.data, include_id=True, include_admin=True)
        return serializer


class PrivateUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, AdministrationPermission)
    queryset = CustomUser.objects.all()
    lookup_field = 'pk'
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = PrivateUserSerializer

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=kwargs['pk'])
        serializer = PrivateUserSerializer(user, include_id=True, include_admin=True)
        return JsonResponse(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = UpdatePrivateUserSerializer(user, data=self.request.data, include_id=True, include_admin=True,
                                                 partial=True)

        if 'id' not in serializer.initial_data:
            raise ParseError('id field is required')
        if int(serializer.initial_data['id']) != pk:
            raise ParseError('id value doesn\'t match')
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data)
