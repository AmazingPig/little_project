from django.db import models
from account_permission.models import User

# Create your models here.

class CodeCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    count = models.IntegerField(verbose_name="代码行数")
    date = models.DateField(auto_now=True, verbose_name="日期")
    file = models.CharField(verbose_name="文件", max_length=510)
    title = models.CharField(verbose_name="标题", max_length=32)

    def __str__(self):
        return str(self.user) + str(self.date)

    class Meta:
        verbose_name = "代码统计表"
        verbose_name_plural = "代码统计表"