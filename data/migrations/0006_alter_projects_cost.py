# Generated by Django 3.2.9 on 2021-11-08 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20211107_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
    ]
