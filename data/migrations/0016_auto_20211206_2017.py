# Generated by Django 3.2.9 on 2021-12-07 01:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0015_auto_20211204_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectattachments',
            name='images',
        ),
        migrations.RemoveField(
            model_name='projectattachments',
            name='project',
        ),
        migrations.AlterUniqueTogether(
            name='projects',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='projects',
            name='action_items',
        ),
        migrations.RemoveField(
            model_name='projects',
            name='images',
        ),
        migrations.RemoveField(
            model_name='projects',
            name='property',
        ),
        migrations.RemoveField(
            model_name='projects',
            name='property_space',
        ),
        migrations.RemoveField(
            model_name='projects',
            name='shared_users',
        ),
        migrations.DeleteModel(
            name='ProjectActionItem',
        ),
        migrations.DeleteModel(
            name='ProjectAttachments',
        ),
        migrations.DeleteModel(
            name='Projects',
        ),
    ]