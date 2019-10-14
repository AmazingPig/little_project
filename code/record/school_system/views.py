from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from .serializers import StudentsSerializer, ClassesSerializer, TeachersSerializer, CoursesSerializer, GradeSerializer
from account_permission.utils import BaseResponse
from django.db.models import F

# Create your views here.


class Students(APIView):

    def get(self, request, cls_id):
        if int(cls_id) == 0:
            student_objs = models.Students.objects.all()
        else:
            student_objs = models.Students.objects.filter(cls_id=cls_id)
        students_ser = StudentsSerializer(student_objs, many=True)

        cls_objs = models.Classes.objects.all()
        cls_ser = ClassesSerializer(cls_objs, many=True)

        ret = {"status": 200, "students": students_ser.data, "classes": cls_ser.data}
        return Response(ret)

    def post(self, request, cls_id):
        ser_obj = StudentsSerializer(data=request.data)
        if ser_obj.is_valid():
            ser_obj.save()
            ret = {"status": 200, "data": "添加成功"}
            return Response(ret)
        return Response(ser_obj.errors)

    def put(self, request, cls_id):
        student_obj = models.Students.objects.filter(id=request.data.get("id")).first()
        ser_obj = StudentsSerializer(data=request.data, instance=student_obj)
        if ser_obj.is_valid():
            ser_obj.save()
            ret = {"status": 200, "data": "编辑成功"}
            return Response(ret)
        return Response(ser_obj.errors)

    def delete(self, request, cls_id):
        student_id = request.data.get("id")
        student_objs = models.Students.objects.filter(id__in=student_id)
        if student_objs:
            for student in student_objs:
                cls = student.cls
                if cls:
                    models.Classes.objects.filter(id=cls.id).update(number=F('number')-1)
                student.delete()
            ret = {"status": 200, "data": "删除成功"}
        else:
            ret = {"status": 441, "data": "班级不存在"}
        return Response(ret)

class Classes(APIView):

    def get(self, request):
        cls_objs = models.Classes.objects.all()
        cls_ser = ClassesSerializer(cls_objs, many=True)

        ret = {"status": 200, "classes": cls_ser.data}
        return Response(ret)

    def post(self, request):
        ser_obj = ClassesSerializer(data=request.data)
        if ser_obj.is_valid():
            ser_obj.save()
            ret = {"status": 200, "data": "添加成功"}
            return Response(ret)
        return Response(ser_obj.errors)

    def put(self, request):
        cls_obj = models.Classes.objects.filter(id=request.data.get("id")).first()
        ser_obj = ClassesSerializer(data=request.data, instance=cls_obj)
        if ser_obj.is_valid():
            ser_obj.save()
            ret = {"status": 200, "data": "编辑成功"}
            return Response(ret)
        return Response(ser_obj.errors)

    def delete(self, request):
        cls_id = request.data.get("id")
        class_objs = models.Classes.objects.filter(id__in=cls_id)
        if class_objs:
            class_objs.delete()
            ret = {"status": 200, "data": "删除成功"}
        else:
            ret = {"status": 440, "data": "班级不存在"}
        return Response(ret)

class Teachers(APIView):

    def get(self, request):
        teacher_objs = models.Teachers.objects.all()
        ser_obj = TeachersSerializer(teacher_objs, many=True)
        ret = {"status": 200, "teachers": ser_obj.data}
        return Response(ret)

    def post(self, request):
        ser_obj = TeachersSerializer(data=request.data)
        if ser_obj.is_valid():
            ser_obj.save()
            ret = {"status": 200, "data": "添加成功"}
            return Response(ret)
        return Response(ser_obj.errors)

    def put(self, request):
        teacher_obj = models.Teachers.objects.filter(id=request.data.get("id")).first()
        ser_obj = TeachersSerializer(data=request.data, instance=teacher_obj)
        if ser_obj.is_valid():
            ser_obj.save()
            ret = {"status": 200, "data": "编辑成功"}
            return Response(ret)
        return Response(ser_obj.errors)

    def delete(self, request):
        teacher_id = request.data.get("id")
        teachers = models.Teachers.objects.filter(id__in=teacher_id)
        if teachers:
            teachers.delete()
            ret = {"status": 200, "data": "删除成功"}
        else:
            ret = {"status": 442, "data": "老师不存在"}
        return Response(ret)

class Courses(APIView):

    def get(self, request, teacher_id):
        if int(teacher_id) == 0:
            course_objs = models.Courses.objects.all()
        else:
            course_objs = models.Courses.objects.filter(teacher_id=teacher_id)

        ser_obj = CoursesSerializer(course_objs, many=True)

        teacher_obj = models.Teachers.objects.all()
        teacher_ser = TeachersSerializer(teacher_obj, many=True)

        cls_obj = models.Classes.objects.all()
        cls_ser = ClassesSerializer(cls_obj, many=True)

        ret = {"status": 200, "courses": ser_obj.data, "teachers": teacher_ser.data, "cls": cls_ser.data}
        return Response(ret)

    def post(self, request, teacher_id):
        ser_obj = CoursesSerializer(data=request.data)
        if ser_obj.is_valid():
            ser_obj.save()
            ret = {"status": 200, "data": "添加成功"}
            return Response(ret)
        return Response(ser_obj.errors)

    def put(self, request, teacher_id):
        course_obj = models.Courses.objects.filter(id=request.data.get("id")).first()
        ser_obj = CoursesSerializer(data=request.data, instance=course_obj)
        if ser_obj.is_valid():
            ser_obj.save()
            ret = {"status": 200, "data": "编辑成功"}
            return Response(ret)
        return Response(ser_obj.errors)

    def delete(self, request, teacher_id):
        courses_id = request.data.get("id")
        course_objs = models.Courses.objects.filter(id__in=courses_id)
        if course_objs:
            course_objs.delete()
            ret = {"status": 200, "data": "删除成功"}
        else:
            ret = {"status": 443, "data": "课程不存在"}
        return Response(ret)

class Grades(APIView):

    def get(self, request):
        course_id = request.query_params.get("course_id")
        student_id = request.query_params.get("student_id")

        if course_id != '0':
            grade_obj = models.Grade.objects.filter(course_id=course_id)
        elif student_id != '0':
            grade_obj = models.Grade.objects.filter(student_id=student_id)

        grade_ser = GradeSerializer(grade_obj, many=True)

        student_obj = models.Students.objects.all()
        student_ser = StudentsSerializer(student_obj, many=True)

        course_obj = models.Courses.objects.all()
        course_ser = CoursesSerializer(course_obj, many=True)

        ret = {"status": 200, "grades": grade_ser.data, "students": student_ser.data, "courses": course_ser.data}
        return Response(ret)

    def post(self, request):
        ser_obj = GradeSerializer(data=request.data)
        if ser_obj.is_valid():
            ser_obj.save()
            ret = {"status": 200, "data": "添加成功"}
            return Response(ret)
        return Response(ser_obj.errors)

    def put(self, request):
        grade_obj = models.Grade.objects.filter(id=request.data.get("id")).first()
        ser_obj = GradeSerializer(data=request.data, instance=grade_obj)
        if ser_obj.is_valid():
            ser_obj.save()
            ret = {"status": 200, "data": "编辑成功"}
            return Response(ret)
        return Response(ser_obj.errors)

    def delete(self, request):
        grades_id = request.data.get("id")
        grade_objs = models.Grade.objects.filter(id__in=grades_id)
        if grade_objs:
            grade_objs.delete()
            ret = {"status": 200, "data": "删除成功"}
        else:
            ret = {"status": 444, "data": "课程不存在"}
        return Response(ret)


