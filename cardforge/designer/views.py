from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics
from rest_framework.response import Response

from designer.models import Game
from designer.permissions import IsOwner
from designer.serializers import GameSerializer, UserSerializer


def login_success(request):
    # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    #
    # if request.user.is_authenticated:
    #     payload = jwt_payload_handler(request.user)
    #     token = jwt_encode_handler(payload)
    #     print(request.user.email)
    #     logout(request)
    #     return redirect("http://cardforge.xyz/home.html?token={}".format(token))
    # else:
    #     return redirect("http://cardforge.xyz")
    return redirect("/")


def home(request):
    context = {}
    return render(request, 'home.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect("http://cardforge.xyz")


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = Game.objects.filter(owners__id=request.user.id)
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        game = serializer.save()
        game.owners.add(self.request.user)


class GameOwners(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, pk):
        queryset = User.objects.filter(games__id=pk)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk', None)
        if pk:
            game = get_object_or_404(Game, pk=pk)
            user = User.objects.filter(email=serializer.data['email']).first()
            if user:
                game.owners.add(user)
                return Response(serializer.data)
            else:
                raise Http404("No User with this email")
        raise Http404("Game doesn't exists")


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwner,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class MeDetail(generics.RetrieveAPIView):
    def retrieve(selfself, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
