# Generated by Django 5.0.7 on 2024-08-06 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('onCourse', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='oncourse_user_groups', to='auth.group'),
        ),
    ]
