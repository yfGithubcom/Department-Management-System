# Generated by Django 4.1.6 on 2023-03-15 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0013_alter_user_user_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='leader',
            new_name='user',
        ),
    ]
