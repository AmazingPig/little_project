from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path('^records/$', views.CodeRecord.as_view()),
    re_path('^get_code_file/$', views.GetCodeFile.as_view())
]