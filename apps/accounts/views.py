from rest_framework import generics, permissions
from .models import Member
from .serializers import MemberSerializer

class SignupView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.AllowAny] # Anyone can sign up

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Returns the profile of the currently logged-in user
        return self.request.user