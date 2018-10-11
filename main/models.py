from django.contrib.auth.models import AbstractUser
from django.db import models


STATUS_WAITING = 0
STATUS_WORKING = 1
STATUS_SUCCESS = 2
STATUS_ERROR = 3

STATUS_CHOICES = ((STATUS_WAITING, 'waiting'), (STATUS_WORKING, 'working'), (STATUS_SUCCESS, 'success'), (STATUS_ERROR, 'error'))


class User(AbstractUser):
    pass


class WikiCategory(models.Model):
    text = models.CharField(unique=True, max_length=500)
    last_fetched = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])


class SeedWikiWebsite(models.Model):
    url = models.CharField(unique=True, max_length=500)
    last_fetched = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])


class Website(models.Model):
    url = models.CharField(unique=True, max_length=500)
    last_fetched = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])


class Feed(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField(unique=True, max_length=500)
    link = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    description = models.TextField()
    version = models.CharField(max_length=10)
    last_fetched = models.DateTimeField(blank=True, null=True)
