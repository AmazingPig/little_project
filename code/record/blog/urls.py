from . import views
from django.urls import path, include, re_path

urlpatterns = [
    re_path('^articles/(?P<author_id>(\d+))/$', views.Articles.as_view()),
    re_path('^article_detail/(?P<article_id>(\d+))/$', views.ArticleDetail.as_view()),
    re_path('^radio/(?P<article_id>(\d+))/$', views.ArticleRadio.as_view()),
    re_path('^like/$', views.Like.as_view()),
    re_path('^category/$', views.Category.as_view()),

]