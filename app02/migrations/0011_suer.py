# Generated by Django 4.1.6 on 2023-03-07 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0010_alter_department_mobile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suer', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
            ],
        ),
    ]
