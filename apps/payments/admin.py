from django.contrib import admin
from django.utils.html import format_html
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # These match your new model fields exactly
    list_display = ("transaction_id", "contributor_name", "amount", "method", "get_status_color", "created_at")
    list_filter = ("status", "method", "created_at")
    search_fields = ("transaction_id", "contributor_name", "phone", "email")
    
    # Readonly fields prevent accidental modification of financial records
    readonly_fields = ("transaction_id", "amount", "method", "created_at", "updated_at", "metadata")

    @admin.display(description="Status")
    def get_status_color(self, obj):
        # Mapping to your STATUS choices (pending, completed, failed)
        colors = {
            "completed": "#27ae60", # Green
            "pending": "#f39c12",   # Orange
            "failed": "#c0392b",    # Red
        }
        return format_html(
            '<b style="color:{}; text-transform: uppercase;">{}</b>', 
            colors.get(obj.status, "black"), 
            obj.status
        )

    def has_add_permission(self, request):
        """Usually, payments should only be created by the system/API, not manually."""
        return False