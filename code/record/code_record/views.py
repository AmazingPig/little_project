import os
import datetime
import zipfile
from . import models
from django.db.models import F
from django.conf import settings
from rest_framework.views import APIView
from account_permission.models import User
from rest_framework.response import Response
from .serializers import CodeCountSerializer
from account_permission.utils import BaseResponse
# Create your views here.

def count_one_file(base_path, file):
    """计算一个文件的代码量"""

    line_count = 0
    file_name_split = file.rsplit(".", maxsplit=1)

    # 判断是否是py文件，只计算py文件
    if len(file_name_split) == 2 and file_name_split[1] == "py":
        file_path = os.path.join(base_path, file)
        with open(file_path, "r", encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    line_count += 1
    return line_count


class CodeRecord(APIView):

    ret = BaseResponse()

    def get(self, request):
        """获取代码记录数据"""
        obj = models.CodeCount.objects.filter(user_id=request.auth.id)
        ser = CodeCountSerializer(obj, many=True)
        ret = {"status": 200, "data": ser.data, "total_count": request.auth.code_count}

        # 获取最近七天的记录用于展示图表
        today = datetime.date.today()
        one_day = datetime.timedelta(days=1)
        date_counts = []  # 七天的代码记录
        date_list = []  # 七天的日期

        # 如果有记录就把当天的记录累加，如果没记录就返回0，最后将列表反转
        for i in range(7):
            idate = today - one_day * i  # 当天的日期
            date_list.append(idate)
            records = models.CodeCount.objects.filter(date=idate, user_id=request.auth.id)
            count = 0
            if records:
                for record in records:
                    count += record.count
            date_counts.append(count)

        date_list.reverse()
        date_counts.reverse()
        ret["date_list"] = date_list
        ret["date_counts"] = date_counts

        return Response(ret)

    def post(self, request):
        """上传文件"""

        zip_file = request.FILES.get("file")

        # 1、判断文件是否是zip格式的压缩文件
        name_split = zip_file.name.rsplit(".", maxsplit=1)
        if len(name_split) != 2 or name_split[1] != "zip":
            self.ret.status = 410
            self.ret.data = "请选择zip格式的压缩文件!"
            return Response(self.ret.dict)

        # 2、将上传的压缩文件保存到本地，并将上传的文件解压，还要防止重名
        target_path = settings.MEDIA_URL + "load_files/" + request.user + "/"
        if not os.path.exists(target_path):
            os.mkdir(target_path)
        path_for_keep = target_path + zip_file.name  # 将要保存下来的zip文件
        path_for_count = target_path + zip_file.name.rsplit(".", maxsplit=2)[0]  # 解压到的目录
        if os.path.exists(path_for_keep):
            self.ret.status = 411
            self.ret.data = "上传的文件名已经存在"
            return Response(self.ret.dict)

        with open(path_for_keep, "wb") as write_f:
            for chunk in zip_file.chunks():
                write_f.write(chunk)

        f = zipfile.ZipFile(zip_file)
        f.extractall(path=path_for_count)
        f.close()

        # 3、统计代码行数
        total_count = 0
        for base_path, dirs, files in os.walk(path_for_count):
            for file in files:
                line_count = count_one_file(base_path, file)
                total_count += line_count

        # 4、写入数据库并将解压后的文件删除
        models.CodeCount.objects.create(user_id=request.auth.id, count=total_count, file=path_for_keep, title=zip_file.name)
        User.objects.filter(id=request.auth.id).update(code_count=F("code_count")+total_count)

        # 先删除目录下的所有文件
        print(path_for_count)
        for base_path, packages, files in os.walk(path_for_count):
            for file in files:
                file_path = os.path.join(base_path, file)
                print(file_path)
                os.remove(file_path)

        # 再递归删除文件夹
        for base_path, packages, files in os.walk(path_for_count):
            for package in packages:
                package_path = os.path.join(base_path, package)
                os.removedirs(package_path)
        os.removedirs(path_for_count)

        # 5、返回给前端
        self.ret.status = 200
        self.ret.data = "上传成功"
        return Response(self.ret.dict)

    def delete(self, request):
        """删除文件和记录"""
        obj_id = request.data.get("id")
        obj = models.CodeCount.objects.filter(id=obj_id).first()
        if obj:
            obj.delete()
            count = obj.count
            User.objects.filter(username=request.user).update(code_count=F('code_count')-count)
            file_path = obj.file
            if os.path.exists(file_path):
                os.remove(file_path)
                self.ret.status = 200
            else:
                self.ret.status = 413
                self.ret.data = "该文件不存在！"
        else:
            self.ret.status = 412
            self.ret.data = "该文件不存在！"
        return Response(self.ret.dict)


class GetCodeFile(APIView):
    ret = BaseResponse()

    def get(self, request):
        """下载文件"""
        obj_id = request.query_params.get("id")
        obj = models.CodeCount.objects.filter(id=obj_id, user_id=request.auth.id).first()
        if obj:
            if os.path.exists(obj.file):
                self.ret.status = 200
                self.ret.data = obj.file
            else:
                self.ret.status = 413
                self.ret.data = "该文件不存在"
        else:
            self.ret.status = 412
            self.ret.data = "该文件不存在！"
        return Response(self.ret.dict)

