# Generated by Django 3.2.9 on 2021-11-08 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20211107_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyspaces',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.properties'),
        ),
    ]
