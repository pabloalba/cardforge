from django.db import models


class Game(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    icon = models.CharField(max_length=255, blank=True)
    owner = models.ForeignKey('auth.User', related_name='games', on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
