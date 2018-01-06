# Generated by Django 2.0.1 on 2018-01-05 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='by_in_colour',
            field=models.CharField(choices=[('w', 'white'), ('b', 'black')], default='w', max_length=1, verbose_name="'by/in' colour"),
        ),
    ]