from django.urls import path
from .views import LatestAnnouncementsView

urlpatterns = [
    path("latest/", LatestAnnouncementsView.as_view(), name="latest-announcements"),
]