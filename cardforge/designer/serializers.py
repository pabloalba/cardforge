from rest_framework import serializers

from designer.models import Game


class GameSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Game
        fields = ('id', 'name', 'icon', 'owner')
