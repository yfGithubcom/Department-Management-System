# Generated by Django 4.1.6 on 2023-02-28 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0003_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app02.department', verbose_name='单位'),
        ),
    ]
