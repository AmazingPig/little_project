from django.db import models
from account_permission.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

# Create your models here.

class Teachers(models.Model):
    """老师表"""
    name = models.CharField(max_length=32, verbose_name="姓名")
    age = models.IntegerField(verbose_name="年龄")

    def __str__(self):
        return self.name


class Goods(models.Model):
    """商品表"""
    title = models.CharField(max_length=32, verbose_name="商品名称")
    brief = models.CharField(max_length=255, verbose_name="简介")
    price = models.FloatField(verbose_name="价格")
    amount = models.IntegerField(verbose_name="库存")
    sail_count = models.IntegerField(verbose_name="销量", default=0)
    img = models.CharField(max_length=510, verbose_name="图片路径", null=True, blank=True)

    coupon = GenericRelation("Coupon")
    order = GenericRelation("Orders")

    def __str__(self):
        return self.title


class Courses(models.Model):
    """课程表"""
    title = models.CharField(max_length=64, verbose_name="课程名称")
    brief = models.CharField(max_length=255, verbose_name="课程简述")
    price = models.FloatField(verbose_name="课程价格")
    sail_count = models.IntegerField(verbose_name="购买人数")
    course_type_choice = ((0, "线上"), (1, "线下"))
    status_choice = ((0, "上线"), (1, "下线"))
    type = models.IntegerField(choices=course_type_choice, verbose_name="课程类型")
    status = models.IntegerField(choices=status_choice, verbose_name="课程状态", default=0)
    img = models.CharField(max_length=510, verbose_name="课程图片", null=True, blank=True)

    def __str__(self):
        return self.title


class CourseDetail(models.Model):
    """课程详细表"""
    course = models.ForeignKey("Courses", verbose_name="课程", on_delete=models.CASCADE)
    teacher = models.ForeignKey("Teachers", verbose_name="老师",on_delete=models.CASCADE)
    hours = models.IntegerField(verbose_name="课时")
    service = models.TextField(verbose_name="你将获得哪些服务")
    study_what = models.TextField(verbose_name="你将学到什么")

    coupon = GenericRelation("Coupon")
    order = GenericRelation("Orders")

    def __str__(self):
        return self.course.title


class CourseCapter(models.Model):
    """课程章节表"""
    course = models.ForeignKey("Courses", verbose_name="课程", on_delete=models.CASCADE)
    chapter = models.IntegerField(verbose_name="第几章", default=1)
    title = models.CharField(max_length=64, verbose_name="标题")

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (("course", "chapter"), )


class Coupon(models.Model):
    """优惠券表"""

    title = models.CharField(max_length=64, verbose_name="优惠券名")
    brief = models.TextField(verbose_name="优惠券介绍", blank=True, null=True)
    coupon_type_choice = (
        (0, "立减券"),
        (1, "满减券"),
        (2, "折扣券")
    )
    coupon_type = models.IntegerField(choices=coupon_type_choice, verbose_name="优惠券类型")

    equal_money = models.FloatField(verbose_name="等值人民币", null=True, blank=True)
    discount = models.IntegerField(verbose_name="折扣百分比", null=True, blank=True, help_text="只有折扣券需要，如78折就填78")
    min_pay = models.IntegerField(verbose_name="最低消费金额", null=True, blank=True, default=0, help_text="针对满减券")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.IntegerField(null=True, blank=True)
    content_obj = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.title


class CouponRecord(models.Model):
    """优惠券领取表"""
    coupon = models.ForeignKey("Coupon", verbose_name="优惠券", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    status_choice = (
        (0, "未使用"),
        (1, "已使用"),
        (2, "已过期")
    )
    status = models.IntegerField(choices=status_choice, verbose_name="状态", default=0)
    order = models.ForeignKey("Orders", verbose_name="关联订单", on_delete=models.CASCADE, null=True, blank=True)


class Orders(models.Model):
    """订单表"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="用户")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField()
    content_obj = GenericForeignKey("content_type", "object_id")

    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    status_choice = (
        (0, "待付款"),
        (1, "已付款"),
        (2, "已取消"),
    )
    status = models.IntegerField(choices=status_choice, verbose_name="订单状态", default=0)

    pay_method_choice = (
        (0, "支付宝"),
        (1, "微信")
    )
    pay_method = models.IntegerField(verbose_name="支付方式", blank=True, null=True)
    pay_number = models.IntegerField(verbose_name="第三方支付单号", blank=True, null=True)
    coupon = models.ForeignKey("Coupon", verbose_name="使用的优惠券", on_delete=models.CASCADE, null=True, blank=True)

    old_money = models.IntegerField(verbose_name="原价")
    new_money = models.IntegerField(verbose_name="实付金额")



