from django.db import models
from account_permission.models import User

# Create your models here.

class Articles(models.Model):
    """文章表"""
    author = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    title = models.CharField(max_length=64, verbose_name="文章标题")
    brief = models.CharField(max_length=255, verbose_name="文章摘要")

    create_time = models.DateField(auto_now_add=True, verbose_name="创建时间")

    like_count = models.IntegerField(verbose_name="点赞数", default=0)
    comment_count = models.IntegerField(verbose_name="评论数", default=0)
    category = models.ForeignKey(to="Category", verbose_name="文章分类", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章表"
        verbose_name_plural = "文章表"

class ArticleContent(models.Model):
    """文章详情表"""
    article = models.ForeignKey(to="Articles", verbose_name="文章", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="文章内容")

    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name_plural = "文章详情表"
        verbose_name = "文章详情表"

class Category(models.Model):
    """分类表"""
    title = models.CharField(max_length=16, verbose_name="分类名", unique=True)
    count = models.IntegerField(verbose_name="当前分类有多少文章", default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="所属用户")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "分类表"
        verbose_name_plural = "分类表"
        unique_together = (("title", "user"),)

class Likes(models.Model):
    """点赞表"""
    user = models.ForeignKey(User, verbose_name="点赞者", on_delete=models.CASCADE)
    article = models.ForeignKey(to="Articles", verbose_name="点赞的文章", on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="点赞时间")

    class Meta:
        unique_together = (("user", "article"),)
        verbose_name = "点赞表"
        verbose_name_plural = "点赞表"

class Comments(models.Model):
    """评论表"""
    user = models.ForeignKey(User, verbose_name="评论者", on_delete=models.CASCADE)
    article = models.ForeignKey(to="Articles", verbose_name="评论文章", on_delete=models.CASCADE)
    content = models.CharField(max_length=255, verbose_name="评论内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")

    parent_comment = models.ForeignKey("self", null=True, on_delete=models.CASCADE, verbose_name="父评论")

    class Meta:
        verbose_name_plural = "评论表"
        verbose_name = "评论表"



