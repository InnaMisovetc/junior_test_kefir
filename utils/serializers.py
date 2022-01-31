from rest_framework import serializers

from users.serializers import BasicUserSerializer
from users_administration.serializers import CitySerializer


class BaseCustomSerializer(serializers.Serializer):
    def to_json(self):
        self.is_valid()
        return self.data


class BadRequestSerializer(BaseCustomSerializer):
    code = serializers.IntegerField()
    message = serializers.CharField()


class InvalidFieldSerializer(serializers.Serializer):
    loc = serializers.ListField(child=serializers.CharField())
    msg = serializers.CharField()
    type = serializers.CharField()


class ValidationErrorSerializer(BaseCustomSerializer):
    detail = InvalidFieldSerializer(many=True)


class PaginationSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    size = serializers.IntegerField()


class HintSerializer(serializers.Serializer):
    city = CitySerializer(many=True)


class MetaSerializer(BaseCustomSerializer):
    pagination = PaginationSerializer()


class PrivateMetaSerializer(BaseCustomSerializer):
    pagination = PaginationSerializer()
    hint = HintSerializer()


class PaginatedResponceSerializer(BaseCustomSerializer):
    data = BasicUserSerializer(many=True)
    meta = MetaSerializer()


class PrivatePaginatedResponceSerializer(BaseCustomSerializer):
    data = BasicUserSerializer(many=True)
    meta = PrivateMetaSerializer()
