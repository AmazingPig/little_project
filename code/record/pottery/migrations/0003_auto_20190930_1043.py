# Generated by Django 2.1.7 on 2019-09-30 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pottery', '0002_auto_20190930_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='price',
            field=models.FloatField(verbose_name='课程价格'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='img',
            field=models.CharField(blank=True, max_length=510, null=True, verbose_name='图片路径'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='price',
            field=models.FloatField(verbose_name='价格'),
        ),
    ]
