# Generated by Django 2.1.2 on 2018-10-25 20:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20181011_1641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='last_fetched',
        ),
        migrations.RemoveField(
            model_name='seedwikiwebsite',
            name='last_fetched',
        ),
        migrations.RemoveField(
            model_name='website',
            name='last_fetched',
        ),
        migrations.RemoveField(
            model_name='wikicategory',
            name='last_fetched',
        ),
        migrations.AddField(
            model_name='feed',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feed',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='seedwikiwebsite',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seedwikiwebsite',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='website',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='website',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='wikicategory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wikicategory',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
