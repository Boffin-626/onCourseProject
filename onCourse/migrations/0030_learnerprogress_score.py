# Generated by Django 5.0.7 on 2024-08-16 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onCourse', '0029_schoolevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='learnerprogress',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
