from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=16, verbose_name="用户名")
    password = models.CharField(max_length=32, verbose_name="密码")
    token = models.CharField(max_length=64, blank=True, null=True)

    sign = models.CharField(max_length=32, null=True, blank=True, verbose_name="个性签名")
    code_count = models.IntegerField(default=0, verbose_name="代码总量")
    article_count = models.IntegerField(default=0, verbose_name="文章数")
    like_count = models.IntegerField(default=0, verbose_name="被点赞数")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "用户表"
        verbose_name = "用户表"