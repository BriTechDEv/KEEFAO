from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Member

@admin.register(Member)
class MemberAdmin(UserAdmin):
    # Fieldsets control the layout of the "Edit User" page
    # We add your custom fields (kcse_year, sponsor_name, etc.) to the 'Personal info' section
    fieldsets = UserAdmin.fieldsets + (
        ("Alumni Details", {"fields": ("kcse_year", "sponsor_name", "registration_fee")}),
    )
    
    # Add fields to the 'Create User' page
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Alumni Details", {"fields": ("kcse_year", "sponsor_name", "registration_fee")}),
    )

    # Columns shown in the main list view
    list_display = ("username", "email", "first_name", "last_name", "kcse_year", "is_staff")
    
    # Filters on the right sidebar
    list_filter = ("kcse_year", "is_staff", "is_superuser", "is_active")
    
    # Search bar configuration
    search_fields = ("username", "first_name", "last_name", "email", "kcse_year")
    
    # Default sorting (Newest KCSE year first)
    ordering = ("-kcse_year", "username")

    # Important: Since you auto-generate usernames from names in models.py,
    # we make sure first_name and last_name are prominent.