# Generated by Django 5.0.7 on 2024-08-11 17:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onCourse', '0020_remove_learnerprogress_concept_grasp_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='school',
            name='contact_email',
            field=models.EmailField(default='example@example.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='school',
            name='principal',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='school',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AddField(
            model_name='school',
            name='district',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='schools', to='onCourse.district'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='DistrictOffice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head', models.CharField(max_length=255)),
                ('contact_email', models.EmailField(default='example@example.com', max_length=254)),
                ('contact_phone', models.CharField(max_length=20)),
                ('district', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='office', to='onCourse.district')),
            ],
        ),
    ]
