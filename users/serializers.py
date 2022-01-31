from rest_framework import serializers

from .models import CustomUser


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


class PrivatePatchUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'city', 'additional_info', 'is_admin')
