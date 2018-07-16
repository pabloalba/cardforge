import os

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics
from rest_framework.response import Response

from .forge import forge_deck
from .models import Deck, Game
from .permissions import IsOwner
from .serializers import GameSerializer, UserSerializer


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


def generate_pdf(request):
    # TODO For test only
    decks = Deck.objects.all()
    file_path = forge_deck(decks[0])
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            # response = HttpResponse(fh.read(), content_type="image/png")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


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
