# Generated by Django 3.2.9 on 2021-12-04 23:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0013_projects_action_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='properties',
            name='zipcode',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(5), django.core.validators.MinLengthValidator(5)]),
        ),
    ]