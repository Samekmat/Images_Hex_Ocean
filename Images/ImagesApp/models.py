import os
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.conf import settings
from PIL import Image as Img
from django.contrib.postgres.fields import ArrayField


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class Image(models.Model):
    name = models.CharField(max_length=120)
    image_url = models.ImageField(upload_to=upload_to)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=upload_to, null=True, blank=True)
    links = ArrayField(models.URLField(max_length=100), null=True, blank=True, default=list)

    def make_thumbnail(self):
        heights = self.profile.plan.sizes.values_list()
        for h in range(len(heights)):
            img = Img.open(self.image_url)
            size = (heights[h][1], heights[h][2])
            img.thumbnail(size, Img.ANTIALIAS)
            thumb_name, thumb_extension = os.path.splitext(self.image_url.name)
            thumb_extension = thumb_extension.lower()
            thumb_filename = thumb_name + f'_thumb_{size}' + thumb_extension

            if thumb_extension in ['.jpg', '.jpeg']:
                FTYPE = 'JPEG'
            elif thumb_extension == '.png':
                FTYPE = 'PNG'
            else:
                return False  # Unrecognized file type

            temp_thumb = BytesIO()
            img.save(temp_thumb, FTYPE)
            temp_thumb.seek(0)
            # set save=False, otherwise it will run in an infinite loop
            self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
            self.links.append(settings.BASE_URL + self.thumbnail.url)
            temp_thumb.close()

        return True

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            raise Exception('Could not create thumbnail - is the file type valid?')
        super(Image, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Size(models.Model):
    height = models.IntegerField()
    width = models.IntegerField(default=200)

    def __str__(self):
        return str(self.height) + 'px'


class Plan(models.Model):
    name = models.CharField(max_length=120)
    sizes = models.ManyToManyField(Size)
    link_to_original = models.BooleanField(default=False)
    expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user}'
