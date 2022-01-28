from rest_framework import serializers

from users.models import CustomUser


class LoginSerializer(serializers.ModelSerializer):
    login = serializers.EmailField(source='email')

    class Meta:
        model = CustomUser
        fields = ('login', 'password')
        extra_kwargs = {'password': {'write_only': True}}
