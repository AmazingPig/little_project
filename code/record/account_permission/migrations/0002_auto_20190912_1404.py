# Generated by Django 2.1.7 on 2019-09-12 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_permission', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='article_count',
            field=models.IntegerField(default=0, verbose_name='文章数'),
        ),
        migrations.AddField(
            model_name='user',
            name='like_count',
            field=models.IntegerField(default=0, verbose_name='被点赞数'),
        ),
        migrations.AlterField(
            model_name='user',
            name='code_count',
            field=models.IntegerField(default=0, verbose_name='代码总量'),
        ),
    ]
