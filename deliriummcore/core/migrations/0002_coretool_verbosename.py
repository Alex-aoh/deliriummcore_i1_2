# Generated by Django 4.1.1 on 2022-10-07 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coretool',
            name='verbosename',
            field=models.CharField(default='null', max_length=30),
            preserve_default=False,
        ),
    ]