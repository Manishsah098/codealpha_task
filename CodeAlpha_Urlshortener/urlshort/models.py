from django.db import models
from django.contrib.auth.models import User


class Url(models.Model):
    long_url = models.URLField()
    short_url = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.long_url