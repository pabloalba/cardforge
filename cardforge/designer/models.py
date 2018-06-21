from django.contrib.auth.models import User
from django.db import models


class Game(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    icon = models.CharField(max_length=255, blank=True)
    owners = models.ManyToManyField(User, related_name='games')

    class Meta:
        ordering = ('name',)
