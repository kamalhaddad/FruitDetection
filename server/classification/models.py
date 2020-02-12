from django.db import models

# Create your models here.

class ClassificationImage(models.Model):
    image = models.ImageField(upload_to='post_images')