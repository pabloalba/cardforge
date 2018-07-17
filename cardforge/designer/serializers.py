from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Deck, Game


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


class GameSerializer(serializers.HyperlinkedModelSerializer):
    owners = serializers.HyperlinkedIdentityField(view_name='game-owners')
    decks = serializers.HyperlinkedIdentityField(view_name='game-decks')

    class Meta:
        model = Game
        fields = ('url', 'name', 'created', 'owners', 'decks')


class DeckSimpleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Deck
        fields = ('url', 'name', 'created', 'size', 'front_cut_marks_color',
                  'back_cut_marks_color', 'portrait')


class DeckSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Deck
        fields = ('url', 'name', 'created', 'size', 'front_cut_marks_color',
                  'back_cut_marks_color', 'portrait', 'cards', 'front_layers', 'back_layers')

