# Generated by Django 2.1.5 on 2019-01-13 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inqapp', '0002_event_event_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_end',
            field=models.DateTimeField(),
        ),
    ]
