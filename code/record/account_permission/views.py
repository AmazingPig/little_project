import uuid
import hashlib
from . import models
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import BaseResponse

# Create your views here.



class Login(APIView):

    ret = BaseResponse()

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        md = hashlib.md5(b'yinwenjie')
        md.update(password.encode("utf-8"))
        user = models.User.objects.filter(username=username, password=md.hexdigest())
        if user:
            self.ret.status = 200
            token = str(uuid.uuid4())
            user.update(token=token)
            self.ret.data = {"token": token, "user_id": user.first().id}
        else:
            self.ret.status = 420
            self.ret.data = "用户名或密码错误"
        return Response(self.ret.dict)

class Logout(APIView):

    ret = BaseResponse()

    def get(self, request):
        request.auth.token = ""
        return Response(self.ret.dict)

class Register(APIView):

    ret = BaseResponse()

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = models.User.objects.filter(username=username)
        if user:
            self.ret.status = 423
            self.ret.data = "该用户名已被注册！"
        elif not username:
            self.ret.status = 424
            self.ret.data = "用户名不能为空！"
        elif len(password) <= 3:
            self.ret.status = 425
            self.ret.data = "密码不能少于4位"
        else:
            token = str(uuid.uuid4())

            # 密码加密
            md = hashlib.md5(b'yinwenjie')
            md.update(password.encode("utf-8"))
            password = md.hexdigest()
            models.User.objects.create(username=username, password=password, token=token)
            self.ret.status = 200
            self.ret.data = token
        return Response(self.ret.dict)

