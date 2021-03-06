# Generated by Django 3.2.9 on 2021-11-28 01:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0011_alter_projects_property_space'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectActionItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=40)),
                ('description', models.TextField(blank=True, null=True)),
                ('images', models.ManyToManyField(blank=True, to='data.Images')),
            ],
        ),
    ]
