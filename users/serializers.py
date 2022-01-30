from rest_framework import serializers

from .models import CustomUser


class BasicUserSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):

        include_id = kwargs.pop('include_id', False)
        include_admin = kwargs.pop('include_admin', False)

        super().__init__(*args, **kwargs)

        if 'id' in self.fields and not include_id:
            self.fields.pop('id')
        if 'is_admin' in self.fields and not include_admin:
            self.fields.pop('is_admin')

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email')


class DetailedUserSerializer(BasicUserSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'is_admin')
        extra_kwargs = {'id': {'read_only': True}}


class PrivateUserSerializer(BasicUserSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'city', 'additional_info', 'is_admin', 'password')
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}


class UpdatePrivateUserSerializer(BasicUserSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'city', 'additional_info', 'is_admin', 'password')
        extra_kwargs = {'password': {'write_only': True}}
