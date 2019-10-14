import time
import redis
from . import models
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from rest_framework.throttling import BaseThrottle


redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='ywj971020', max_connections=10)


class BaseResponse:
    status = 200
    data = ""

    @property
    def dict(self):
        return {"status": self.status, "data": self.data}


class LoginAuth(BaseAuthentication):
    def authenticate(self, request):
        """
        登陆认证，获取token与登录时写进数据库的token进行比较
        如果没有token说明没有登陆过，如果请求地址是login或register则直接通过。
        """

        if request.path == "/login/" or request.path == "/register/":
            return
        token = request.GET.get("token", "")
        if not token:
            raise AuthenticationFailed({"status": 421, "data": "请登录！"})
        username = request.GET.get("username","")
        user = models.User.objects.filter(username=username, token=token).first()
        if not user:
            raise AuthenticationFailed({"status": 422, "data": "请登录！"})
        return user.username, user


VISIT_RECORD = {}

class ThrottleControl(BaseThrottle):
    """一分钟允许访问一百次"""

    pass_time = 60  # 限定时间
    allow_times = 100  # 限定次数
    history_record = []  # 当前用户的访问记录

    def allow_request(self, request, view):
        ip = request.META.get("REMOTE_ADDR")
        now = time.time()
        # 1.判断当前ip是否曾经访问过，是否在字典中
        if ip not in VISIT_RECORD:
            VISIT_RECORD[ip] = [now, ]
            return True

        # 2.如果访问过，取出访问记录，并添加一条记录
        history_record = VISIT_RECORD[ip]
        history_record.insert(0, now)
        self.history_record = history_record

        # 3.判断记录中最早的一次和这一次相比是否超过过期时间
        while history_record[0] - history_record[-1] > self.pass_time:
            history_record.pop()

        # 3.判断记录中的访问次数是否超过规定次数
        if len(history_record) > self.allow_times:
            return False
        return True

    def wait(self):
        # 返回还需要等待的时间
        wait_time = self.pass_time - (self.history_record[0] - self.history_record[-1])
        return wait_time

