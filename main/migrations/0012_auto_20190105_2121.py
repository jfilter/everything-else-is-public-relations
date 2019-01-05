# Generated by Django 2.1.5 on 2019-01-05 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20181026_1817'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posts_per_day', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WebsiteScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reddits_per_day', models.FloatField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='feed',
            name='posts_per_day',
        ),
        migrations.RemoveField(
            model_name='website',
            name='reddits_per_day',
        ),
        migrations.AddField(
            model_name='websitescore',
            name='website',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Website'),
        ),
        migrations.AddField(
            model_name='feedscore',
            name='feed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Feed'),
        ),
    ]