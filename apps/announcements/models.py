from django.db import models

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False) # New field
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'announcements'
        # Pinned items first, then newest by date
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title
    
