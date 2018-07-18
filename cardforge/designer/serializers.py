from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Deck, Game

import json


class JSONSerializerField(serializers.Field):
    def to_representation(self, value):
        json_data = {}
        try:
            json_data = json.loads(value)
        except ValueError as e:
            raise e
        finally:
            return json_data

    def to_internal_value(self, data):
        return json.dumps(data)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


class GameSerializer(serializers.HyperlinkedModelSerializer):
    owners = serializers.HyperlinkedIdentityField(view_name='game-owners')
    decks = serializers.HyperlinkedIdentityField(view_name='game-decks')

    class Meta:
        model = Game
        fields = ('id', 'url', 'name', 'created', 'owners', 'decks')


class DeckSimpleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Deck
        fields = ('id', 'url', 'name', 'created', 'size', 'front_cut_marks_color',
                  'back_cut_marks_color', 'portrait')


class DeckSerializer(serializers.HyperlinkedModelSerializer):
    cards = JSONSerializerField()
    front_layers = JSONSerializerField()
    back_layers = JSONSerializerField()

    class Meta:
        model = Deck
        fields = ('id', 'url', 'name', 'created', 'size', 'front_cut_marks_color',
                  'back_cut_marks_color', 'portrait', 'cards', 'front_layers', 'back_layers', 'trunks')

