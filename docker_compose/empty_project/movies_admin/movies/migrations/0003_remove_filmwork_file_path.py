# Generated by Django 3.2 on 2023-04-19 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_rename_modified_at_to_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filmwork',
            name='file_path',
        ),
    ]
