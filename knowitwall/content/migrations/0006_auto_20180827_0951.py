# Generated by Django 2.0.1 on 2018-08-27 09:51

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_episode_second_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='transcript',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='le transcript', null=True),
        ),
    ]
