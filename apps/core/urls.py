from django.urls import path, include

urlpatterns = [
    # Core app's own URLs (e.g., site settings)
    # path("settings/", SiteSettingsView.as_view(), name="site-settings"),

    # Including all other apps under the 'api/' prefix
    path("accounts/", include("apps.accounts.urls")),
    path("events/", include("apps.events.urls")),
    path("contributions/", include("apps.contributions.urls")),
    path("payments/", include("apps.payments.urls")),
    path("gallery/", include("apps.gallery.urls")),
]