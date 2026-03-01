from rest_framework import generics
from .models import GalleryImage
from .serializers import GallerySerializer

class GalleryListView(generics.ListAPIView):

    queryset = GalleryImage.objects.all()
    serializer_class = GallerySerializer