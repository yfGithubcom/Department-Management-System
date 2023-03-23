# Generated by Django 4.1.1 on 2022-10-19 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=32, verbose_name='学校')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32, verbose_name='用户')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('salary', models.IntegerField(verbose_name='薪水')),
                ('account', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='账户余额')),
                ('gender', models.SmallIntegerField(choices=[(0, '女'), (1, '男')], verbose_name='性别')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app02.department')),
            ],
        ),
    ]
