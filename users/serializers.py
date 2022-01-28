from rest_framework import serializers

from .models import CustomUser


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            not_allowed = set(exclude)
            for exclude_name in not_allowed:
                self.fields.pop(exclude_name)


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'other_name', 'email', 'phone', 'birthday', 'is_admin')
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}
