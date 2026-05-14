from django.shortcuts import render
from rest_framework.decorators import api_view, action
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from .models import *
from .serializers import *
from games.models import Game
from games.serializers import GameSerializer
from django.db.models import Q
from .selectors import TeamSelector


# Create your views here.
@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Teams': '/teams/',
        'Players': '/players/',
        'Player Stats': '/player-stats/',
        'Team Stats': '/team-stats/',
    }
    return Response(api_urls)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by('team_name')
    serializer_class = TeamSerializer

    @action(detail=True, methods=['get'])
    def roster(self, request, pk=None):
        # players = Player.objects.filter(
        #     team_id=pk,
        #     active=True,
        #     ).select_related('team').exclude(jersey__isnull=True)
        
        players = TeamSelector.roster(pk)
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"], url_path="games")
    def games(self, request, pk=None):
        team = self.get_object()

        # games = Game.objects.filter(
        #     Q(home_team=team) | Q(away_team=team)
        # ).select_related("home_team", "away_team", "victor").order_by("date")
        
        games = TeamSelector.games(team)
        serializer = GameSerializer(
            games,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.select_related('team').all().order_by('team__team_name', 'name')
    serializer_class = PlayerSerializer


class PlayerStatViewSet(viewsets.ModelViewSet):
    queryset = PlayerStat.objects.select_related('player', 'team', 'player__team').all().order_by('team')
    serializer_class = PlayerStatSerializer

# class RosterViewSet(generics.ListAPIView):
#     serializer_class = PlayerSerializer

#     def get_queryset(self):
#         return Player.objects.filter(
#             team_id = self.kwargs["team_id"]
#         ).select_related("team")