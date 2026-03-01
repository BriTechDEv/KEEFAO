from django.db import models

class SiteSetting(models.Model):
    """
    Holds global site settings or configuration.
    Useful for values like site title, contact email, or announcement banners.
    """
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'core'

    def __str__(self):
        return f"{self.key} = {self.value}"