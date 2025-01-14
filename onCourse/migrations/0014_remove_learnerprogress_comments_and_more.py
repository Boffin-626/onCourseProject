# Generated by Django 5.0.7 on 2024-08-09 14:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onCourse', '0013_learnerprogress_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learnerprogress',
            name='comments',
        ),
        migrations.AddField(
            model_name='learner',
            name='background_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='learnerprogress',
            name='subject',
            field=models.CharField(default='subject', max_length=100),
        ),
        migrations.CreateModel(
            name='TeacherComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('progress_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='onCourse.learnerprogress')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onCourse.teacher')),
            ],
        ),
    ]
