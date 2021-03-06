# Generated by Django 2.0.1 on 2018-08-27 21:19

import ckeditor.fields
from django.db import migrations, models
import team.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='le name', max_length=200)),
                ('role', models.CharField(default='role within Knowitwall', max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to=team.models.teammember_image_directory_path)),
                ('bio', ckeditor.fields.RichTextField(default='le bio')),
            ],
        ),
    ]
