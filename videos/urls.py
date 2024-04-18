from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path("check_url/", views.check_url, name="youtube_check_url"),
    path("infos/", views.infos, name="youtube_infos"),
    path("videos/", views.videos, name="youtube_videos"),
    path("statistics/videos/", views.statistics_videos, name="youtube_statistics_videos"),
    path("statistics/channels/", views.statistics_channels, name="youtube_statistics_channels"),
]