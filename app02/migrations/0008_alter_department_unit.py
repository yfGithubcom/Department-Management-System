# Generated by Django 4.1.6 on 2023-03-03 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0007_department_mobile_alter_department_unit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='unit',
            field=models.CharField(max_length=32, unique=True, verbose_name='部门名称'),
        ),
    ]
