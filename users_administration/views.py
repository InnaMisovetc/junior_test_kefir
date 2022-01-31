from http.client import responses

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser
from users.serializers import BasicUserSerializer, CreateUserSerializer, PrivatePatchUserSerializer
from users_administration.pagination import AdminCustomPagination
from utils.serializers import BadRequestSerializer, ValidationErrorSerializer, PrivatePaginatedResponceSerializer
from .permissions import AdministrationPermission


@method_decorator(name='get',
                  decorator=extend_schema(
                      responses={
                          200: OpenApiResponse(response=PrivatePaginatedResponceSerializer, description=responses[200]),
                          400: OpenApiResponse(response=BadRequestSerializer, description=responses[400]),
                          401: OpenApiResponse(response=OpenApiTypes.STR, description=responses[401]),
                          403: OpenApiResponse(response=OpenApiTypes.STR, description=responses[403]),
                          422: OpenApiResponse(response=ValidationErrorSerializer, description=responses[422])}))
@method_decorator(name='post',
                  decorator=extend_schema(
                      request=CreateUserSerializer,
                      responses={
                          201: OpenApiResponse(response=CreateUserSerializer, description=responses[201]),
                          400: OpenApiResponse(response=BadRequestSerializer, description=responses[400]),
                          401: OpenApiResponse(response=OpenApiTypes.STR, description=responses[401]),
                          403: OpenApiResponse(response=OpenApiTypes.STR, description=responses[403]),
                          422: OpenApiResponse(response=ValidationErrorSerializer, description=responses[422])}))
class PrivateUsersListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, AdministrationPermission)
    queryset = CustomUser.objects.all().order_by('id')
    pagination_class = AdminCustomPagination

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'GET':
            serializer = BasicUserSerializer(self.paginate_queryset(self.queryset), many=True)
        else:
            serializer = CreateUserSerializer(data=self.request.data)
        return serializer


@method_decorator(name='get',
                  decorator=extend_schema(
                      responses={
                          200: OpenApiResponse(response=CreateUserSerializer, description=responses[200]),
                          400: OpenApiResponse(response=BadRequestSerializer, description=responses[400]),
                          401: OpenApiResponse(response=OpenApiTypes.STR, description=responses[401]),
                          403: OpenApiResponse(response=OpenApiTypes.STR, description=responses[403]),
                          422: OpenApiResponse(response=ValidationErrorSerializer, description=responses[422])}))
@method_decorator(name='patch',
                  decorator=extend_schema(
                      request=PrivatePatchUserSerializer,
                      responses={
                          201: OpenApiResponse(response=PrivatePatchUserSerializer, description=responses[201]),
                          400: OpenApiResponse(response=BadRequestSerializer, description=responses[400]),
                          401: OpenApiResponse(response=OpenApiTypes.STR, description=responses[401]),
                          403: OpenApiResponse(response=OpenApiTypes.STR, description=responses[403]),
                          404: OpenApiResponse(response=OpenApiTypes.STR, description=responses[404]),
                          422: OpenApiResponse(response=ValidationErrorSerializer, description=responses[422])}))
@method_decorator(name='delete',
                  decorator=extend_schema(
                      request=PrivatePatchUserSerializer,
                      responses={
                          204: OpenApiResponse(description=responses[204]),
                          401: OpenApiResponse(response=OpenApiTypes.STR, description=responses[401]),
                          403: OpenApiResponse(response=OpenApiTypes.STR, description=responses[403]),
                          422: OpenApiResponse(response=ValidationErrorSerializer, description=responses[422])}))
class PrivateUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, AdministrationPermission)
    queryset = CustomUser.objects.all()
    lookup_field = 'pk'
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = CreateUserSerializer

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=kwargs['pk'])
        serializer = CreateUserSerializer(user)
        return JsonResponse(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = PrivatePatchUserSerializer(user, data=self.request.data, partial=True)

        if 'id' not in serializer.initial_data:
            raise ParseError('id field is required')
        if int(serializer.initial_data['id']) != pk:
            raise ParseError('id value doesn\'t match')
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data)
