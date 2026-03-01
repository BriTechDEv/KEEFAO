from rest_framework import generics, permissions
from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer

class EventListView(generics.ListAPIView):

    queryset = Event.objects.all()
    serializer_class = EventSerializer


class RegisterEventView(generics.CreateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventRegistrationSerializer

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)