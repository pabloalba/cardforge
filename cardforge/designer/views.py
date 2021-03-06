import json
import os

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .forge import forge_card_to_png, forge_deck as forge_deck_method
from .models import Deck, Game
from .permissions import IsOwner
from .serializers import DeckSerializer, DeckSimpleSerializer, GameSerializer, UserSerializer


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


@require_http_methods("POST")
@transaction.atomic
def clone_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    decks = list(game.decks.all())
    owners = list(game.owners.all())

    game.id = None
    game.name = "{0}_Copy".format(game.name)
    game.save(force_insert=True)
    game.owners.add(*owners)

    for deck in decks:
        deck.game = game
        deck.id = None
        deck.save(force_insert=True)

    serializer = GameSerializer(game, many=False, context={"request": request})
    return JsonResponse(serializer.data)


@require_http_methods("POST")
@transaction.atomic
def clone_deck(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    deck.id = None
    deck.name = "{0}_Clone".format(deck.name)
    deck.save(force_insert=True)

    serializer = DeckSerializer(deck, many=False, context={"request": request})
    return JsonResponse(serializer.data)


def forge_card(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    try:
        num = int(request.GET.get('num', 0))
    except:
        num = 0
    front = request.GET.get('front', '').lower() == 'true'
    file_path = forge_card_to_png(deck, num, front)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="image/png")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def forge_deck(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    export_format = request.GET.get('export_format', 'pdf')
    export_target = request.GET.get('export_target', 'standard')
    export_type = request.GET.get('export_type', 'a4')

    file_path = forge_deck_method(deck, export_type=export_type, export_format=export_format,
                                  export_target=export_target)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            if export_format == 'pdf':
                response = HttpResponse(fh.read(), content_type="application/pdf")
            else:
                response = HttpResponse(fh.read(), content_type="image/png")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def update_layers(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    data = json.loads(request.body)
    if data.get('front', False):
        deck.front_layers = data['layers']
    else:
        deck.back_layers = data['layers']
    deck.save()
    return JsonResponse({})


def update_cards(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    data = json.loads(request.body)
    deck.cards = data['cards']
    deck.save()
    return JsonResponse({})


@login_required
def logout(request):
    auth_logout(request)
    return redirect("/")


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'me': reverse('me', request=request, format=format),
        'games': reverse('game-list', request=request, format=format)
    })


class MeDetail(generics.RetrieveAPIView):
    def retrieve(selfself, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = Game.objects.filter(owners__id=request.user.id).annotate(n_decks=Count("decks"))
        serializer = GameSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        game = serializer.save()
        game.owners.add(self.request.user)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwner,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer


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


class GameDecks(generics.ListCreateAPIView):
    queryset = Deck.objects.all()
    serializer_class = DeckSimpleSerializer

    def list(self, request, pk):
        queryset = Deck.objects.filter(game__id=pk)
        serializer = DeckSimpleSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        game = Game.objects.filter(id=self.kwargs.get('pk', None)).first()
        if not game:
            raise Http404("Game doesn't exists")
        serializer.save(
            game=game,
            cards="[]",
            front_layers="[]",
            back_layers="[]"
        )


class DeckDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer
