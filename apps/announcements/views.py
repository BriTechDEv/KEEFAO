from rest_framework import generics
from .models import Announcement
from .serializers import AnnouncementSerializer

class AnnouncementListView(generics.ListAPIView):

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer


class LatestAnnouncementsView(generics.ListAPIView):
    """
    Returns the latest 5 announcements, prioritizing pinned items.
    """
    serializer_class = AnnouncementSerializer
    # This view is public so anyone visiting the landing page can see it
    permission_classes = [] 

    def get_queryset(self):
        return Announcement.objects.all()[:5]