# Generated by Django 4.1.1 on 2022-10-10 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_brandcore_corebrand_rename_orgcore_coreorg'),
    ]

    operations = [
        migrations.AddField(
            model_name='corebrand',
            name='description',
            field=models.CharField(default='Descripciones', max_length=300),
            preserve_default=False,
        ),
    ]
