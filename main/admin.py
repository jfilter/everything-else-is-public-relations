from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, WikiCategory, SeedWikiWebsite, Feed, Website, STATUS_WAITING


class DateAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', )


admin.site.register(User, UserAdmin)
admin.site.register(WikiCategory, DateAdmin)
admin.site.register(SeedWikiWebsite, DateAdmin)


def delete_feeds(modeladmin, request, queryset):
    queryset.all().delete()


delete_feeds.short_description = "delete all feeds"


class FeedAdmin(DateAdmin):
    list_display = ['created_at', 'url', 'website']
    ordering = ['-created_at']
    actions = [delete_feeds]


admin.site.register(Feed, FeedAdmin)


def reset_websites(modeladmin, request, queryset):
    queryset.update(status=STATUS_WAITING)


reset_websites.short_description = "reset website"


class WebsiteAdmin(DateAdmin):
    list_display = ['created_at', 'status']
    ordering = ['-created_at']
    actions = [reset_websites]


admin.site.register(Website, WebsiteAdmin)
