from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from rest_framework.routers import DefaultRouter
from games.views import GameViewSet


router = DefaultRouter()

router.register(r"players", PlayerViewSet)
router.register(r"teams", TeamViewSet)
router.register(r"player-stats", PlayerStatViewSet)
# router.register(r"game-stats", GameStatViewSet)
router.register(r"games", GameViewSet, basename="game")

urlpatterns = [
    path("", include(router.urls)),
    path("games/", include("games.urls")),
]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)