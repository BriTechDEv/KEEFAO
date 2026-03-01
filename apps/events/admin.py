from django.contrib import admin
from django.utils.html import format_html
from .models import Event, EventRegistration


#see a list of registered members directly inside the Event page
class RegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # What you see in the list view
    list_display = ("title", "date", "location")
    inlines = [RegistrationInline]
    # Filter by date and location on the right sidebar
    list_filter = ("date", "location")
    # Search by title or description
    search_fields = ("title", "description")
    # Sort by upcoming events first
    ordering = ("date",)

@admin.display(description="Status")
def colored_status(self, obj):
        colors = {
            'DRAFT': '#7f8c8d',     # Gray
            'UPCOMING': '#2980b9',  # Blue
            'ONGOING': '#27ae60',   # Green
            'COMPLETED': '#f39c12', # Orange
            'CANCELLED': '#c0392b', # Red
        }
        color = colors.get(obj.status, '#000')
        return format_html(
            '<b style="color:{};">{}</b>',
            color,
            obj.get_status_display()
        )

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    # Showing the member name and the event they joined
    list_display = ("member", "event", "registered_at")
    
    # Filter by events to see who joined a specific one
    list_filter = ("event", "registered_at")
    
    # Search for a specific member by username or email
    search_fields = ("member__username", "member__email", "event__title")
    
    # Make registration date read-only
    readonly_fields = ("registered_at",)