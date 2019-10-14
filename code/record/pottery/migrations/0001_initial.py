# Generated by Django 2.1.7 on 2019-09-30 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('account_permission', '0003_user_sign'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='优惠券名')),
                ('brief', models.TextField(blank=True, null=True, verbose_name='优惠券介绍')),
                ('coupon_type', models.IntegerField(choices=[(0, '立减券'), (1, '满减券'), (2, '折扣券')], verbose_name='优惠券类型')),
                ('equal_money', models.FloatField(blank=True, null=True, verbose_name='等值人民币')),
                ('discount', models.IntegerField(blank=True, help_text='只有折扣券需要，如78折就填78', null=True, verbose_name='折扣百分比')),
                ('min_pay', models.IntegerField(blank=True, default=0, help_text='针对满减券', null=True, verbose_name='最低消费金额')),
                ('object_id', models.IntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='CouponRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, '未使用'), (1, '已使用'), (2, '已过期')], default=0, verbose_name='状态')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pottery.Coupon', verbose_name='优惠券')),
            ],
        ),
        migrations.CreateModel(
            name='CourseCapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.IntegerField(default=1, verbose_name='第几章')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
            ],
        ),
        migrations.CreateModel(
            name='CourseDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.IntegerField(verbose_name='课时')),
                ('service', models.TextField(verbose_name='你将获得哪些服务')),
                ('study_what', models.TextField(verbose_name='你将学到什么')),
            ],
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='课程名称')),
                ('brief', models.CharField(max_length=255, verbose_name='课程简述')),
                ('price', models.IntegerField(verbose_name='课程价格')),
                ('type', models.IntegerField(choices=[(0, '线上课程'), (1, '线下课程')], verbose_name='课程类型')),
                ('status', models.IntegerField(choices=[(0, '上线'), (1, '下线')], default=0, verbose_name='课程状态')),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='商品名称')),
                ('brief', models.CharField(max_length=255, verbose_name='简介')),
                ('price', models.IntegerField(verbose_name='价格')),
                ('amount', models.IntegerField(verbose_name='库存')),
                ('img', models.CharField(max_length=510, verbose_name='图片路径')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField()),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('status', models.IntegerField(choices=[(0, '待付款'), (1, '已付款'), (2, '已取消')], default=0, verbose_name='订单状态')),
                ('pay_method', models.IntegerField(blank=True, null=True, verbose_name='支付方式')),
                ('pay_number', models.IntegerField(verbose_name='第三方支付单号')),
                ('old_money', models.IntegerField(verbose_name='原价')),
                ('new_money', models.IntegerField(verbose_name='实付金额')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pottery.Coupon', verbose_name='使用的优惠券')),
                ('user', models.ForeignKey(default='用户', on_delete=django.db.models.deletion.CASCADE, to='account_permission.User')),
            ],
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('age', models.IntegerField(verbose_name='年龄')),
            ],
        ),
        migrations.AddField(
            model_name='coursedetail',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pottery.Courses', verbose_name='课程'),
        ),
        migrations.AddField(
            model_name='coursedetail',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pottery.Teachers', verbose_name='老师'),
        ),
        migrations.AddField(
            model_name='coursecapter',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pottery.Courses', verbose_name='课程'),
        ),
        migrations.AddField(
            model_name='couponrecord',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pottery.Orders', verbose_name='关联订单'),
        ),
        migrations.AddField(
            model_name='couponrecord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_permission.User', verbose_name='用户'),
        ),
        migrations.AlterUniqueTogether(
            name='coursecapter',
            unique_together={('course', 'chapter')},
        ),
    ]
