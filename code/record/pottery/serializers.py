from . import models
from rest_framework import serializers

class GoodsSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Goods
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):

    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return obj.get_type_display()


    class Meta:
        model = models.Courses
        fields = "__all__"

class CouponSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Coupon
        fields = ['id', 'title', 'brief']

class CouponRecordSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.coupon.title

    class Meta:
        model = models.CouponRecord
        fields = ["id", "title", ]