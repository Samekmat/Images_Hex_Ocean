from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Image
from .serializers import ImageSerializer


class ImageUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageListViewSet(LoginRequiredMixin, ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()

    def get_queryset(self):
        return self.queryset.filter(profile=self.request.user.profile)
