# Generated by Django 2.1.2 on 2018-10-10 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20181010_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='seedwikiwebsite',
            name='status',
            field=models.IntegerField(choices=[(0, 'waiting'), (1, 'working'), (2, 'success'), (3, 'error')], default=0),
        ),
        migrations.AddField(
            model_name='wikicategory',
            name='status',
            field=models.IntegerField(choices=[(0, 'waiting'), (1, 'working'), (2, 'success'), (3, 'error')], default=0),
        ),
    ]
