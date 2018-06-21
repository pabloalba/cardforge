from django.contrib.auth.models import User
from rest_framework import serializers

from designer.models import Deck, Game


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'name', 'icon')


class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
