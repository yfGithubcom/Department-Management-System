# Generated by Django 4.1.6 on 2023-03-15 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0014_rename_leader_task_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app02.su', verbose_name='领导'),
        ),
    ]
