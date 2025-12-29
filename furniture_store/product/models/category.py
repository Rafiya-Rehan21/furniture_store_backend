from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    def __str__(self):
        return self.title
