"""The main application's URLs."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("stats", views.stats, name="stats"),
    path("feeds", views.feeds_index, name="feeds"),
    path('feeds/<slug:slug>/', views.feeds_detail)]
