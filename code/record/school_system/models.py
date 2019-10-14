from django.db import models

# Create your models here.

class Classes(models.Model):
    title = models.CharField(max_length=16, verbose_name="班级名称")
    number = models.IntegerField(verbose_name="班级人数", default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "班级表"
        verbose_name_plural = "班级表"

class Students(models.Model):
    number = models.CharField(max_length=32, verbose_name="学号")
    name = models.CharField(max_length=16, verbose_name="学生姓名")
    age = models.IntegerField(verbose_name="学生年龄")
    hometown = models.CharField(max_length=32, verbose_name="学生家乡")

    cls = models.ForeignKey("Classes", verbose_name="所属班级", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Courses(models.Model):
    title = models.CharField(max_length=32, verbose_name="课程名称")
    cls = models.ForeignKey("Classes", verbose_name="所属班级", on_delete=models.CASCADE)
    teacher = models.ForeignKey("Teachers", verbose_name="任课老师", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Teachers(models.Model):
    name = models.CharField(max_length=16, verbose_name="老师姓名")
    age = models.IntegerField(verbose_name="老师年龄")

    def __str__(self):
        return self.name

class Grade(models.Model):
    """成绩表"""
    course = models.ForeignKey("Courses", verbose_name="课程", on_delete=models.CASCADE)
    student = models.ForeignKey("Students", verbose_name="学生", on_delete=models.CASCADE)

    grade = models.IntegerField(verbose_name="成绩")
    note = models.TextField(verbose_name="评语", null=True, blank=True)

    class Meta:
        unique_together = (('course', 'student'),)
