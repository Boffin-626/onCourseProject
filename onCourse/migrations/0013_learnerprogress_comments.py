# Generated by Django 5.0.7 on 2024-08-09 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onCourse', '0012_remove_learnerprogress_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='learnerprogress',
            name='comments',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]