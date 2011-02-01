from django.db import models

class InterestGroup(models.Model):
    name = models.CharField(max_length=70, blank=False)
    public = models.BooleanField(default=True)
    slug = models.SlugField(max_length=70, blank=True)

