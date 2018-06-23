from django.contrib.auth.models import User
from django.db import models


class Game(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    icon = models.CharField(max_length=255, blank=True)
    owners = models.ManyToManyField(User, related_name='games')

    class Meta:
        ordering = ('name',)


class Deck(models.Model):
    DECK_SIZES = (
        ('S', 'standard'),
        ('M', 'mini'),
        ('B', 'big'),
        ('R', 'bridge'),
        ('Q', 'squared'),
    )
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    icon = models.CharField(max_length=255, blank=True)
    game = models.ForeignKey(Game, related_name='decks', on_delete=models.CASCADE)
    size = models.CharField(max_length=1, choices=DECK_SIZES)
    same_reverse = models.BooleanField(null=False, default=True)
    front_border_color = models.CharField(max_length=7, blank=False, null=False, default="#000000")
    front_cut_marks_color = models.CharField(max_length=7, blank=False, null=False, default="#FF0000")
    back_border_color = models.CharField(max_length=7, blank=False, null=False, default="#000000")
    back_cut_marks_color = models.CharField(max_length=7, blank=False, null=False, default="#FF0000")
    cards = models.TextField()  # json data
    front_layers = models.TextField()  # json data
    back_layers = models.TextField()  # json data

    class Meta:
        ordering = ('name',)
