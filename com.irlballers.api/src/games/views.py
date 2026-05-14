from django.shortcuts import render
from rest_framework import viewsets
from games.serializers import *
from .models import *

# Create your views here.
class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.select_related(
        "home_team",
        "away_team",
        "victor"
    ).order_by('date')
    serializer_class = GameSerializer


# class TeamGameViewSet(viewsets.ModelViewSet):
#     queryset = Game.objects.select_related(
#         "home_team",
#         "home_score"
#         "away_team",
#         "away_score"
#         "victor"
#     ).filter(home_team=).order_by('date')