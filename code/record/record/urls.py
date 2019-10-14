"""record URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from account_permission import views as a_views
from django.views.static import serve
from django.urls import path, include, re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    # 账户相关代码
    re_path('^login/$', a_views.Login.as_view()),
    re_path('^logout/$', a_views.Logout.as_view()),
    re_path('^register/$', a_views.Register.as_view()),

    # 春泥造物url
    re_path('^api/pottery/', include('pottery.urls')),

    # 代码统计url
    re_path('^api/code/', include('code_record.urls')),

    # 博客功能url
    re_path('^api/blog/', include('blog.urls')),

    # 教务系统url
    re_path('^api/school/', include('school_system.urls')),

    # 其他功能url
    # re_path('^api/others/', include('other_functions.urls')),

    # media路径配置
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]


