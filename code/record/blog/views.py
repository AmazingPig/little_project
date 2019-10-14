from . import models
from aip import AipSpeech
from django.conf import settings
from bs4 import BeautifulSoup
from django.db.models import F
from .serializers import ArticleSerializer, CategorySerializer, ArticleDetailSerializer
from django.shortcuts import render
from account_permission.utils import BaseResponse
from account_permission.models import User
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.

class Articles(APIView):
    """文章信息"""
    def get(self, request, author_id):

        if int(author_id) == 0:
            # 获取所有文章
            articles = models.Articles.objects.all()
            articles_ser = ArticleSerializer(articles, many=True)
        else:
            # 获取该用户的所有文章
            articles = models.Articles.objects.filter(author_id=author_id)
            articles_ser = ArticleSerializer(articles, many=True)

        if not articles:
            ret = {"status": 430, "data": "还没有写过文章"}
            return Response(ret)

        # 获取该用户点赞前十名的文章
        like_articles_ser = articles.order_by("like_count").reverse()[0:5]
        likes_ser = ArticleSerializer(like_articles_ser, many=True)

        # 获取该用户的分类
        category = models.Category.objects.filter(user_id=request.auth.id).order_by("count").reverse()[0:5]
        category_ser = CategorySerializer(category, many=True)

        ret = {"status": 200,
               "articles": articles_ser.data,
               "likes": likes_ser.data,
               "categories": category_ser.data,
               "sign": request.auth.sign,
               "like_count": request.auth.like_count,
               "article_count": request.auth.article_count,
               "author_id": author_id,
               }

        return Response(ret)

    def post(self, request, author_id):
        author = User.objects.filter(id=author_id)
        if not author:
            ret = {"status": 432, "data": "该用户不存在"}
            return Response(ret)

        # 获取标题和内容
        title = request.data.get("title", "")
        content = request.data.get("content", "")

        if not title or not content:
            ret = {"status": 433, "data": "文章标题或内容不能为空"}
            return Response(ret)

        article = models.Articles.objects.filter(title=title, author_id=author_id)
        if article:
            ret = {"status": 436, "data": "文章名已存在"}
            return Response(ret)

        # 获取选择的分类
        category_id = request.data.get("category_id", "")
        if category_id:
            category = models.Category.objects.filter(id=int(category_id), user_id=request.auth.id)
            if not category:
                ret = {"status": 435, "data": "分类不存在"}
                return Response(ret)
            article = models.Articles.objects.create(author_id=author_id, title=title, brief=content[0:100], category_id=category_id)
            category.update(count=F('count')+1)
        else:
            article = models.Articles.objects.create(author_id=author_id, title=title, brief=content[0:100])

        models.ArticleContent.objects.create(article=article, content=content)
        User.objects.filter(id=author_id).update(article_count=F("article_count")+1)

        ret = {"status": 200, "data": "创建成功"}

        return Response(ret)

    def delete(self, request, author_id):
        article_id = request.data.get("article_id", "")
        article = models.Articles.objects.filter(id=article_id, author_id=author_id)

        if not article:
            ret = {"status": 434, "data": "该文章不存在"}
            return Response(ret)

        if article.first().category:
            models.Category.objects.filter(id=article.first().category_id).update(count=F('count')-1)  # 更新分类表

        article.delete()
        User.objects.filter(id=author_id).update(article_count=F('article_count')-1)  # 更新用户表
        models.Likes.objects.filter(article_id=article_id).delete()  # 更新点赞表
        models.Comments.objects.filter(article_id=article_id).delete()  # 更新评论表

        ret = {"status": 200, "data": "删除成功"}

        return Response(ret)

    def put(self, request, author_id):

        # 获取文章ID、标题、内容和分类ID
        article_id = request.data.get("id", "")
        title = request.data.get("title", "")
        content = request.data.get("content", "")
        category_id = request.data.get("category_id", "")
        article = models.Articles.objects.filter(id=article_id)

        if not title or not content:
            ret = {"status": 433, "data": "文章内容或标题不能为空"}
        elif not article:
            ret = {"status": 434, "data": "文章不存在"}
        else:
            if_article = models.Articles.objects.filter(title=title, author_id=request.auth.id)
            if if_article and if_article.first().id != article_id:
                ret = {"status": 436, "data": "该文章名已经存在"}
                return Response(ret)

            # 判断分类是否存在。首先判断原来是否有分类，如果有就先把这个分类文章数量-1。再判断是否传了新分类id
            old_category = article.first().category
            if old_category:
                old_category.count = old_category.count-1  # 原来的分类文章数-1
                old_category.save()
            if not category_id:
                article.update(title=title, brief=content[0:100], category_id=None)
            else:
                new_category = models.Category.objects.filter(id=category_id, user_id=request.auth.id)  # 新的分类
                if not new_category:
                    ret = {"status": 435, "data": "分类不存在"}
                    return Response(ret)
                article.update(title=title, brief=content[0:100], category_id=category_id)
                new_category.update(count=F("count")+1)

            models.ArticleContent.objects.filter(article=article.first()).update(content=content)
            ret = {"status": 200, "data": "编辑成功"}

        return Response(ret)


class ArticleDetail(APIView):
    """文章详情"""
    def get(self, request, article_id):
        # 获取文章详情
        article_obj = models.ArticleContent.objects.filter(article_id=article_id).first()
        article_ser = ArticleDetailSerializer(article_obj)

        # 获取作者文章点赞排行
        author = article_obj.article.author
        like_articles = models.Articles.objects.filter(author_id=author.id).order_by("like_count").reverse()[0: 5]
        like_articles_ser = ArticleSerializer(like_articles, many=True)

        # 获取作者的分类
        category = models.Category.objects.filter(user_id=author.id).order_by("count").reverse()[0:5]
        category_ser = CategorySerializer(category, many=True)

        # 获取用户是否点赞该文章
        is_like = False
        like_record = models.Likes.objects.filter(user_id=request.auth.id, article_id=article_id)
        if like_record:
            is_like = True

        ret = {"status": 200,
               "article_detail": article_ser.data,
               "like_articles": like_articles_ser.data,
               "categories": category_ser.data,
               "is_like": is_like,
               }
        return Response(ret)


class ArticleRadio(APIView):
    """文章音频"""
    def get(self, request, article_id):
        obj = models.ArticleContent.objects.filter(article_id=article_id).first()
        html = obj.content  # 获取数据库中保存的html
        soup = BeautifulSoup(html, 'lxml')
        text = soup.get_text()  # 从html提取文本

        # 利用百度语音合成生成音频
        APP_ID = '17358840'
        API_KEY = 'EIjvIwWGg4XfdnSu4U0GyVEo'
        SECRET_KEY = 'sKOg333AsYzU7mv0omU244aW95f25tyM'

        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

        result = client.synthesis(text, 'zh', 1, {'per': 3, 'vol': 5})

        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if not isinstance(result, dict):
            path = settings.MEDIA_URL + 'radio/' + obj.article.title + '.mp3'  # media/radio/xxxx.mp3
            with open(path, 'wb') as f:
                f.write(result)

        ret = {"status": 200, "data": path}
        return Response(ret)



class Like(APIView):
    """点赞或取消点赞"""
    def post(self, request):
        article_id = request.data.get("article_id", 0)
        user_id = request.auth.id
        author_id = models.Articles.objects.filter(id=article_id).first().author_id
        like_obj = models.Likes.objects.filter(user_id=user_id, article_id=article_id)
        if like_obj:
            like_obj.delete()
            User.objects.filter(id=author_id).update(like_count=F('like_count')-1)  # 给作者的总点赞数-1
            models.Articles.objects.filter(id=article_id).update(like_count=F('like_count')-1)  # 给这篇文章点赞数-1
            ret = {"status": 430, "data": False}
        else:
            models.Likes.objects.create(user_id=user_id, article_id=article_id)
            User.objects.filter(id=author_id).update(like_count=F('like_count')+1)  # 给作者的总点赞数+1
            models.Articles.objects.filter(id=article_id).update(like_count=F('like_count')+1)  # 给这篇文章点赞数+1
            ret = {"status": 200, "data": True}
        return Response(ret)

class Category(APIView):
    """分类"""
    def get(self, request):
        category = models.Category.objects.filter(user_id=request.auth.id)
        category_ser = CategorySerializer(category, many=True)
        ret = {"status": 200, "data": category_ser.data}
        return Response(ret)

    def post(self, request):
        title = request.data.get("title", "")
        if title:
            obj = models.Category.objects.filter(user=request.auth, title=title)
            if obj:
                ret = {"status": 431, "data": "该分类已经存在！"}
            else:
                models.Category.objects.create(user=request.auth, title=title)
                category = models.Category.objects.filter(user_id=request.auth.id).order_by("count").reverse()[0:5]
                category_ser = CategorySerializer(category, many=True)
                ret = {"status": 200, "data": "创建分类成功！", "categories": category_ser.data}
            return Response(ret)

    def delete(self, request):
        category_id = int(request.data.get("category_id", 0))
        category = models.Category.objects.filter(id=category_id, user=request.auth)

        if not category:
            ret = {"status": 435, "data": "该分类不存在"}
            return Response(ret)

        models.Articles.objects.filter(category_id=category_id).update(category_id=None)  # 将该分类下的文章更新
        category.delete()

        ret = {"status": 200, "data": "删除成功"}
        return Response(ret)

    def put(self, request):
        category_id = request.data.get("category_id", 0)
        category = models.Category.objects.filter(id=category_id, user_id=request.auth.id)
        if not category:
            ret = {"status": 435, "data": "该分类不存在"}
            return Response(ret)

        title = request.data.get("category_title", "")
        category = models.Category.objects.filter(title=title, user_id=request.auth.id)
        if category and category.first().id != category_id:
            ret = {"status": 437, "data": "该分类已存在"}
            return Response(ret)

        models.Category.objects.filter(id=category_id).update(title=title)
        ret = {"status": 200, "data": "编辑成功"}
        return Response(ret)





