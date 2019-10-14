from django.urls import re_path
from . import views

urlpatterns = [
    re_path('^goods/$', views.Goods.as_view()),
    re_path('^courses/$', views.Courses.as_view()),
    re_path('^coupons/$', views.Coupon.as_view()),

    re_path('^shopping_car/$', views.ShoppingCar.as_view()),
    re_path('^orders/$', views.Order.as_view()),
    re_path('^pay/$', views.Pay.as_view())
]