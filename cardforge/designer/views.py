from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from designer.models import Game
from designer.permissions import IsOwner
from designer.serializers import GameSerializer


def login_success(request):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    if request.user.is_authenticated:
        payload = jwt_payload_handler(request.user)
        token = jwt_encode_handler(payload)
        return redirect("http://cardforge.net/home.html?token={}".format(token))
    else:
        return redirect("http://cardforge.net")


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = Game.objects.filter(owner=request.user)
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwner,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer
