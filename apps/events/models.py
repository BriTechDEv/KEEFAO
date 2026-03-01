from django.db import models
from apps.accounts.models import Member

class Event(models.Model):

    # Define the choices inside the class
    class EventStatus(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        UPCOMING = "UPCOMING", "Upcoming/Open"
        ONGOING = "ONGOING", "Ongoing"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=EventStatus.choices,
        default=EventStatus.DRAFT,
    )

    class Meta:
        app_label = 'events'

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class EventRegistration(models.Model):

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)