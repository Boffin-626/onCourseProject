# Generated by Django 5.0.7 on 2024-08-11 17:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onCourse', '0021_district_school_contact_email_school_principal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='districtoffice',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='onCourse.user'),
            preserve_default=False,
        ),
    ]