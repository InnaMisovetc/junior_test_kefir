from rest_framework import serializers

from users.models import CustomUser


class CitySerializer(serializers.Serializer):
    id = serializers.IntegerField(source='city.id')
    name = serializers.CharField(source='city.name')

    class Meta:
        model = CustomUser
        fields = ('id', 'name')
