import random
from django.contrib.auth.models import AbstractUser
from django.db import models

class Member(AbstractUser):
    # null=True and blank=True allow these can be filled in later
    sponsor_name = models.CharField(max_length=255, null=True, blank=True)
    kcse_year = models.IntegerField(null=True, blank=True)
    registration_fee = models.IntegerField(default=200)

    class Meta:
        app_label = 'accounts'

    # This list tells the terminal which extra fields to ask for 
    # during 'createsuperuser'. 
    REQUIRED_FIELDS = ['email'] 

    def save(self, *args, **kwargs):
        if not self.username and self.first_name and self.last_name:
            base_username = f"{self.first_name}{self.last_name}".lower().replace(" ", "")
            username = base_username
            
            # Check if username exists and loop until a unique one is found
            while Member.objects.filter(username=username).exists():
                username = f"{base_username}{random.randint(100, 999)}"
            
            self.username = username
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username