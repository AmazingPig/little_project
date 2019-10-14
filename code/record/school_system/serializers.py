from rest_framework import serializers
from . import models
from django.db.models import F

class StudentsSerializer(serializers.ModelSerializer):

    cls_obj = serializers.SerializerMethodField(read_only=True)

    def get_cls_obj(self, obj):
        cls_obj = models.Classes.objects.filter(id=obj.cls_id).first()
        return cls_obj.title

    def create(self, validated_data):
        student_obj = models.Students.objects.create(**validated_data)
        models.Classes.objects.filter(id=student_obj.cls_id).update(number=F('number')+1)
        return student_obj

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.age = validated_data.get("age", instance.age)
        instance.number = validated_data.get("number", instance.number)
        instance.cls = validated_data.get("cls", instance.cls)
        instance.hometown = validated_data.get("hometown", instance.hometown)
        instance.save()
        return instance

    class Meta:
        model = models.Students
        fields = '__all__'

class ClassesSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        cls_obj = models.Classes.objects.create(**validated_data)
        return cls_obj

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.number = validated_data.get("number", instance.number)
        instance.save()
        return instance

    class Meta:
        model = models.Classes
        fields = '__all__'

class TeachersSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        teacher_obj = models.Teachers.objects.create(**validated_data)
        return teacher_obj

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.age = validated_data.get("age", instance.age)
        instance.save()
        return instance

    class Meta:
        model = models.Teachers
        fields = '__all__'

class CoursesSerializer(serializers.ModelSerializer):

    cls_title = serializers.SerializerMethodField(read_only=True)
    teacher_name = serializers.SerializerMethodField(read_only=True)

    def get_cls_title(self, obj):
        return obj.cls.title

    def get_teacher_name(self, obj):
        return obj.teacher.name

    def create(self, validated_data):
        obj = models.Courses.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.cls = validated_data.get("cls", instance.cls)
        instance.teacher = validated_data.get("teacher", instance.teacher)
        instance.save()
        return instance

    class Meta:
        model = models.Courses
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):

    course_title = serializers.SerializerMethodField(read_only=True)
    student_name = serializers.SerializerMethodField(read_only=True)

    def get_course_title(self, obj):
        return obj.course.title

    def get_student_name(self, obj):
        return obj.student.name

    def create(self, validated_data):
        obj = models.Grade.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        instance.student = validated_data.get("student", instance.student)
        instance.course = validated_data.get("course", instance.course)
        instance.grade = validated_data.get("grade", instance.grade)
        instance.note = validated_data.get("note", instance.note)
        instance.save()
        return instance

    class Meta:
        model = models.Grade
        fields = '__all__'
