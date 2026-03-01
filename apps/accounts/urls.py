from django.urls import path, include
from .views import SignupView, UserProfileView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    
    # Password Reset endpoints (provided by the library)
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]