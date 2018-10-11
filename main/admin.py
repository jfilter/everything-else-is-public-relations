from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, WikiCategory, SeedWikiWebsite, Feed, Website

admin.site.register(User, UserAdmin)

admin.site.register(WikiCategory)
admin.site.register(SeedWikiWebsite)
admin.site.register(Feed)
admin.site.register(Website)
