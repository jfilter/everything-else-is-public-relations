from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

STATUS_WAITING = 0
STATUS_WORKING = 1
STATUS_SUCCESS = 2
STATUS_ERROR = 3

STATUS_CHOICES = (
    (STATUS_WAITING, "waiting"),
    (STATUS_WORKING, "working"),
    (STATUS_SUCCESS, "success"),
    (STATUS_ERROR, "error"),
)


class User(AbstractUser):
    pass


class WikiCategory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.CharField(unique=True, max_length=500)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    def __str__(self):
        return self.text


class SeedWikiWebsite(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.CharField(unique=True, max_length=500)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    def __str__(self):
        return self.url


class Website(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    slug = models.SlugField(null=True)
    title = models.CharField(max_length=500, null=True)
    description = models.TextField(null=True)
    url = models.CharField(unique=True, max_length=500)
    reddits_per_day = models.FloatField(null=True)

    def __repr__(self):
        return f"{self.url}, {self.status}, {self.updated_at}, {self.created_at}"

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.url)

        super(Website, self).save(*args, **kwargs)


class WebsiteScore(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    reddits_per_day = models.FloatField(null=True)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)


class Feed(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, null=True, blank=True
    )
    url = models.CharField(unique=True, max_length=500)
    link = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    description = models.TextField()
    version = models.CharField(max_length=10)
    posts_per_day = models.FloatField(null=True)

    def __str__(self):
        return self.url


class FeedScore(models.Model):
    posts_per_day = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
