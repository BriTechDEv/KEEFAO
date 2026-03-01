from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from .models import Contribution

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    # Updated: Changed 'created_at' to 'date' and added 'payment_reference'
    list_display = ("contributor_name", "category", "amount", "colored_status", "payment_reference", "date")
    
    # Updated: Changed 'created_at' to 'date'
    list_filter = ("status", "category", "date")
    
    # Updated: Added payment_reference for better tracking
    search_fields = ("contributor_name", "phone", "email", "payment_reference")
    
    # Updated: Changed 'created_at' to 'date'
    readonly_fields = ("date", "payment_reference")
    
    actions = ["mark_as_verified"]

    @admin.display(description="Status")
    def colored_status(self, obj):
        colors = {
            'PENDING': '#f39c12',  # Orange
            'VERIFIED': '#27ae60', # Green
            'FAILED': '#c0392b',   # Red
        }
        color = colors.get(obj.status, '#000')
        return format_html(
            '<b style="color:{};">{}</b>',
            color,
            obj.get_status_display()
        )

    @admin.action(description="Mark selected contributions as Verified")
    def mark_as_verified(self, request, queryset):
        queryset.update(status='VERIFIED')
        self.message_user(request, "Selected contributions marked as Verified.")

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        
        try:
            # cl is the ChangeList instance which contains the filtered queryset
            cl = response.context_data['cl']
            qs = cl.queryset
            total = qs.filter(status='VERIFIED').aggregate(Sum('amount'))['amount__sum'] or 0
            count = qs.count()
            
            # Add variables to the context for your custom template
            response.context_data['total_amount'] = f"{total:,}" 
            response.context_data['total_count'] = count
        except (AttributeError, KeyError, TypeError):
            # Fallback if context_data isn't available (e.g., on redirects)
            pass
        
        return response