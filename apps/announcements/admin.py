from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    # 'created_at' is useful to see when it was posted
    list_display = ("title", "is_pinned", "created_at", "short_content")
    
    # Allows you to find specific announcements quickly
    search_fields = ("title", "content")
    
    # Filter by date on the right sidebar
    list_filter = ("created_at",)
    
    # Sort by newest first
    ordering = ("-created_at",)

    # Custom method to show a snippet of the content in the list view
    @admin.display(description="Content Snippet")
    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content