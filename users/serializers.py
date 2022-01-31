from rest_framework import serializers

from .models import CustomUser
from django.contrib.auth.hashers import make_password


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email')


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'is_admin')


class PatchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday')
        extra_kwargs = {'id': {'read_only': True}}


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'city', 'additional_info', 'is_admin', 'password')
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(CreateUserSerializer, self).create(validated_data)


class PrivatePatchUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'city', 'additional_info', 'is_admin')
