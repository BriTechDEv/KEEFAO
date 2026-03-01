from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryImage

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    # 'image_preview' shows the actual thumbnail in the list
    list_display = ("title", "image_preview")
    search_fields = ("title",)

    @admin.display(description="Preview")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: auto; border-radius: 5px;" />',
                obj.image.url
            )
        return "No Image"