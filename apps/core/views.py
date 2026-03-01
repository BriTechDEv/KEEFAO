from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SiteSetting
import logging

core_logger = logging.getLogger("core")

class SiteSettingsView(APIView):
    """
    Returns all site settings for the frontend or admin dashboard.
    """
    def get(self, request):
        try:
            settings_qs = SiteSetting.objects.all()
            data = {s.key: s.value for s in settings_qs}
            core_logger.info("Site settings fetched successfully", extra={"count": settings_qs.count()})
            return Response(data)
        except Exception as e:
            core_logger.error("Failed to fetch site settings", exc_info=True)
            return Response({"error": "Could not retrieve site settings"}, status=500)