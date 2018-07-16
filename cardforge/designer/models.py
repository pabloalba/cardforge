from django.contrib.auth.models import User
from django.db import models


class Game(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    owners = models.ManyToManyField(User, related_name='games')

    class Meta:
        ordering = ('name',)


class Deck(models.Model):
    DECK_SIZES = (
        ('SE', 'standard euro'),
        ('ME', 'mini euro'),
        ('SA', 'standard american'),
        ('MA', 'mini american')
    )
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    game = models.ForeignKey(Game, related_name='decks', on_delete=models.CASCADE)
    size = models.CharField(max_length=2, choices=DECK_SIZES)
    front_cut_marks_color = models.CharField(max_length=7, blank=False, null=False, default="#FF0000")
    back_cut_marks_color = models.CharField(max_length=7, blank=False, null=False, default="#FF0000")
    cards = models.TextField(default="{}")  # json data
    front_layers = models.TextField(default="{}")  # json data
    back_layers = models.TextField(default="{}")  # json data

    class Meta:
        ordering = ('name',)
