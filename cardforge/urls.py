from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from .designer import views as designer_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("social_django.urls", namespace="social")),

    path("auth/login", auth_views.login, name="login"),
    path("auth/login/success", designer_views.login_success, name="login-success"),
    path("auth/logout", designer_views.logout, name="logout"),

    path("", designer_views.home, name="home"),
    path("api", designer_views.api_root, name="api-root"),
    path("api/me", designer_views.MeDetail.as_view(), name="me"),
    path("api/games", designer_views.GameList.as_view(), name="game-list"),
    path("api/games/<int:pk>", designer_views.GameDetail.as_view(), name="game-detail"),
    path("api/games/<int:pk>/_clone", designer_views.clone_game, name="game-clone"),
    path("api/games/<int:pk>/owners", designer_views.GameOwners.as_view(), name="game-owners"),
    path("api/games/<int:pk>/decks", designer_views.GameDecks.as_view(), name="game-decks"),

    path("api/decks/<int:pk>", designer_views.DeckDetail.as_view(), name="deck-detail"),
    path("api/decks/<int:pk>/_clone", designer_views.clone_deck, name="deck-clone"),
    path("api/decks/<int:pk>/layers", designer_views.update_layers, name="deck-update-layers"),
    path("api/decks/<int:pk>/cards", designer_views.update_cards, name="deck-update-cards"),
    path("api/decks/<int:pk>/forge_card", designer_views.forge_card, name="forge-card"),
    path("api/decks/<int:pk>/forge_deck", designer_views.forge_deck, name="forge-deck"),
]
