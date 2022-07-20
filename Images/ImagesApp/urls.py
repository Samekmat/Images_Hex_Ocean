from django.urls import path

from .views import ImageListViewSet, ImageUpload

urlpatterns = [
    path('list', ImageListViewSet.as_view({'get': 'list'}), name='image-list'),
    path('upload', ImageUpload.as_view(), name='image-upload'),
]
