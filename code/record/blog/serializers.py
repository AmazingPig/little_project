from . import models
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        author_obj = obj.author
        return {"username": author_obj.username, "id": author_obj.id}

    class Meta:
        model = models.Articles
        exclude = ['category', ]

class ArticleDetailSerializer(serializers.ModelSerializer):

    article = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        author_obj = obj.article.author
        return {
            "id": author_obj.id,
            "author_name": author_obj.username,
            "sign": author_obj.sign
        }

    def get_article(self, obj):
        article_obj = obj.article
        category_title = article_obj.category.title if article_obj.category_id else ""
        category_id = article_obj.category_id if article_obj.category_id else ""
        return {
            "id": article_obj.id,
            "author": article_obj.author.username,
            "title": article_obj.title,
            "create_time": article_obj.create_time,
            "like_count": article_obj.like_count,
            "category": category_title,
            "category_id": category_id
        }


    class Meta:
        model = models.ArticleContent
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        exclude = ['user', ]
