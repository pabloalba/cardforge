from django.contrib.auth.models import User
from django.db import models


class Game(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    owners = models.ManyToManyField(User, related_name='games')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Deck(models.Model):
    DECK_SIZES = (
        ('PO', 'estandar poker 63x88'),
        ('B1', 'bridge 56x88'),
        ('B2', 'bridge 57x89'),
        ('M1', 'mini 41x68'),
        ('M2', 'mini 45x68'),
        ('M3', 'mini 44x63'),
        ('C1', 'cuadrada 68x68'),
        ('C2', 'cuadrada 70x70'),
        ('TA', 'tarot 70x110'),
        ('GR', 'grande 70x120')
    )
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    game = models.ForeignKey(Game, related_name='decks', on_delete=models.CASCADE)
    size = models.CharField(max_length=2, choices=DECK_SIZES)
    front_cut_marks_color = models.CharField(max_length=7, blank=False, null=False, default="#FF0000")
    back_cut_marks_color = models.CharField(max_length=7, blank=False, null=False, default="#FF0000")
    portrait = models.BooleanField(default=False)
    cards = models.TextField(default="[]")  # json data
    front_layers = models.TextField(default="[]")  # json data
    back_layers = models.TextField(default="[]")  # json data

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
