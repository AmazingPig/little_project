from django.urls import re_path
from . import views

urlpatterns = [
    re_path('^students/(?P<cls_id>(\d+))/$', views.Students.as_view()),
    re_path('^classes/$', views.Classes.as_view()),
    re_path('^teachers/$', views.Teachers.as_view()),
    re_path('^courses/(?P<teacher_id>(\d+))/$', views.Courses.as_view()),
    re_path('^grades/$', views.Grades.as_view()),
]