# Generated by Django 2.1.5 on 2019-02-06 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inqapp', '0010_customuser_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='last_updated',
            field=models.DateTimeField(null=True),
        ),
    ]
