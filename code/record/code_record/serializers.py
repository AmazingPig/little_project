from . import models
from rest_framework import serializers

class CodeCountSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField(read_only=True)
    count = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        user_obj = obj.user
        return user_obj.username

    def get_count(self, obj):
        return str(obj.count)

    class Meta:
        model = models.CodeCount
        exclude = ["file", ]

        extra_kwargs = {"user": {"write_only": True}}