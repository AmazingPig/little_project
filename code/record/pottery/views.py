import json
import redis
from . import models
from .utils.pay import AliPay
from django.conf import settings
from account_permission.utils import redis_pool
from .serializers import GoodsSerializer, CourseSerializer, CouponSerializer, CouponRecordSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class Goods(APIView):
    def get(self, request):
        goods_obj = models.Goods.objects.all().order_by("sail_count")[:3]  # 获取销量前三的商品
        goods_ser = GoodsSerializer(goods_obj, many=True)
        ret = {"status": 200, "goods": goods_ser.data}
        return Response(ret)


class Courses(APIView):
    def get(self, request):
        courses_obj = models.Courses.objects.filter(status=0).order_by("sail_count")[:3]  # 获取销量前三的课程
        courses_ser = CourseSerializer(courses_obj, many=True)
        ret = {"status": 200, "courses": courses_ser.data}
        return Response(ret)


class Coupon(APIView):
    def get(self, request):
        user_id = request.query_params.get("id", 0)
        if user_id:
            coupon_record_objs = models.CouponRecord.objects.filter(user_id=request.auth.id, status=0)
            coupon_ser = CouponRecordSerializer(coupon_record_objs, many=True)
        else:
            coupon_objs = models.Coupon.objects.all()
            coupon_ser = CouponSerializer(coupon_objs, many=True)

        ret = {"status": 200, "coupons": coupon_ser.data}
        return Response(ret)

    def post(self, request):
        coupon_id = request.data.get('id', 0)

        coupon_record_obj = models.CouponRecord.objects.filter(coupon_id=coupon_id, user_id=request.auth.id)
        if coupon_record_obj:
            ret = {"status": 450, "data": "已领取过优惠券"}
            return Response(ret)

        models.CouponRecord.objects.create(coupon_id=coupon_id, user_id=request.auth.id)
        ret = {"status": 200, "data": "领取成功"}
        return Response(ret)


class ShoppingCar(APIView):

    conn = redis.Redis(connection_pool=redis_pool)

    def get(self, request):
        key = settings.SHOPPING_CAR_KEY % request.user  # shopping_car_username
        value = json.loads(self.conn.get(key))


        course_objs = models.Courses.objects.filter(id__in=value["course"])
        course_ser = CourseSerializer(course_objs, many=True)
        good_objs = models.Goods.objects.filter(id__in=value["good"])
        good_ser = GoodsSerializer(good_objs, many=True)

        ret = {"status": 200, "courses": course_ser.data, "goods": good_ser.data}
        return Response(ret)


    def post(self, request):
        # 1.获取前端传来的type和id
        type = request.data.get("type", "")
        id = request.data.get("id", 0)

        course_obj = None
        good_obj = None

        # 2.检验数据合法性
        if type == "course":
            course_obj = models.Courses.objects.filter(id=id)
            if not course_obj:
                ret = {"status": 452, "data": "课程不存在"}
                return Response(ret)
            elif course_obj.first().status == 1:
                ret = {"status": 454, "data": "该课程已下线"}
                return Response(ret)
        elif type == "good":
            good_obj = models.Goods.objects.filter(id=id)
            if not good_obj:
                ret = {"status": 453, "data": "商品不存在"}
                return Response(ret)
            elif good_obj.first().amount == 0:
                ret = {"status": 455, "data": "该商品暂时无货"}
                return Response(ret)
        else:
            ret = {"status": 451, "data": "请输入正确的数据格式"}
            return Response(ret)

        # 3.去redis中获取当前用户的购物车信息
        key = settings.SHOPPING_CAR_KEY % request.user  # shopping_car_username
        value = self.conn.get(key)

        # 4.构建存入redis的购物车信息
        if not value:
            new_value = {"course": [], "good": []}
        else:
            new_value = json.loads(value)

        if course_obj and id not in new_value["course"]:
            new_value["course"].append(id)
        elif good_obj and id not in new_value["good"]:
            new_value["good"].append(id)

        new_value = json.dumps(new_value)

        if new_value.encode("utf-8") == value:
            ret = {"status": 456, "data": "已在购物车中"}
            return Response(ret)

        self.conn.set(key, new_value)
        ret = {"status": 200, "data": "加入购物车成功"}
        return Response(ret)


    def delete(self, request):
        type = request.data.get("type", "")
        choice_id = int(request.data.get("id", 0))

        key = settings.SHOPPING_CAR_KEY % request.user
        value = json.loads(self.conn.get(key))  # 获取该用户购物车信息
        print(value)
        course_list = value["course"]
        good_list = value["good"]

        if type == "course":
            obj = models.Courses.objects.filter(id=choice_id)
            if not obj:
                ret = {"status": 459, "data": "课程或商品不存在"}
                return Response(ret)
            if choice_id not in course_list:
                ret = {"status": 460, "data": "不在购物车中"}
                return Response(ret)
            course_list.remove(choice_id)

        elif type == "good":
            obj = models.Goods.objects.filter(id=choice_id)
            if not obj:
                ret = {"status": 459, "data": "课程或商品不存在"}
                return Response(ret)
            if choice_id not in good_list:
                ret = {"status": 460, "data": "不在购物车中"}
                return Response(ret)
            good_list.remove(choice_id)

        else:
            ret = {"status": 451, "data": "未选择类型或id"}
            return Response(ret)

        new_value = json.dumps({"course": course_list, "good": good_list})
        self.conn.set(key, new_value)

        ret = {"status": 200, "data": "删除成功"}
        return Response(ret)


class Pay(APIView):

    def post(self, request):

        # 1.获取数据
        type = request.data.get("type")  # 课程还是商品
        choice_id = request.data.get("choice_id")
        price = request.data.get("price")
        coupon_id = request.data.get("coupon", 0)
        payment = request.data.get("payment")  # 付款方式，1代表支付宝，2代表微信

        # 2.校验数据
        if type == "course":
            obj = models.Courses.objects.filter(id=choice_id, status=0)
            if not obj:
                ret = {"status": 452, "data": "课程不存在"}
                return Response(ret)
        elif type == "good":
            obj = models.Goods.objects.filter(id=choice_id)
            if not obj:
                ret = {"status": 453, "data": "商品不存在"}
                return Response(ret)
            if obj.first().amount == 0:
                ret = {"status": 455, "data": "库存不足"}
                return Response(ret)
        else:
            ret = {"status": 451, "data": "未选择种类或id"}
            return Response(ret)

        if obj.first().price != price:
            ret = {"status": 457, "data": "价格错误"}
            return Response(ret)

        # 3.计算使用优惠券后的价格
        if coupon_id != 0:
            coupon_obj = models.CouponRecord.objects.filter(id=coupon_id, status=0)
            if not coupon_obj:
                ret = {"status": 458, "data": "优惠券无效"}
                return Response(ret)

            # 判断优惠券类型
            coupon_type = coupon_obj.first().coupon.coupon_type
            if coupon_type == 0:  # 立减券
                new_price = price - coupon_obj.first().coupon.equal_money
            elif coupon_type == 1:  # 满减券
                if price >= coupon_obj.first().coupon.min_pay:
                    new_price = price - coupon_obj.first().coupon.equal_money
                else:
                    ret = {"status": 458, "data": "优惠券无效"}
                    return Response(ret)
            elif coupon_type == 2:  # 折扣券
                new_price = price * coupon_obj.first().coupon.discount * 0.01
        else:
            new_price = price

        # 4.创建订单
        order_obj = models.Orders.objects.create(user_id=request.auth.id, content_obj=obj.first(), old_money=price,
                                                 new_money=new_price)

        # 5.调用支付宝接口
        if payment == "1":
            alipay = AliPay(
                appid='2016092000554424',
                app_notify_url='http://60.205.227.178:8000/api/pottery/order',
                return_url='http://60.205.227.178:8000/api/pottery/order',
                app_private_key_path='pottery/utils/app_private_2048.txt',
                alipay_public_key_path='pottery/utils/alipay_public_2048.txt',  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
                debug=True,  # 默认False,
            )
            # 生成支付的url
            query_params = alipay.direct_pay(
                subject=obj.first().title,  # 商品简单描述
                out_trade_no=order_obj.id,  # 商户订单号
                total_amount=new_price,  # 交易金额(单位: 元)
            )
            pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)

        ret = {"status": 200, "pay_url": pay_url}
        return Response(ret)


class Order(APIView):
    pass
