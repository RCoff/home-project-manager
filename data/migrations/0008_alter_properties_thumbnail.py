# Generated by Django 3.2.9 on 2021-11-09 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_auto_20211107_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='properties',
            name='thumbnail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.images'),
        ),
    ]
