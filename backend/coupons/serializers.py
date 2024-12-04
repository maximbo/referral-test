from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer


@extend_schema_serializer(component_name="Простой ответ с полем detail")
class MessageSerializer(serializers.Serializer):
    detail = serializers.CharField()
