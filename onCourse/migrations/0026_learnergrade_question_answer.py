# Generated by Django 5.0.7 on 2024-08-13 04:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onCourse', '0025_teacher_subjects'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearnerGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=10)),
                ('concept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onCourse.concept')),
                ('learner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onCourse.learner')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=255)),
                ('concept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onCourse.concept')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=255)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onCourse.question')),
            ],
        ),
    ]