import rest_framework.serializers as serializers
from .models import *
from src.settings import SITE_URL




class TeamSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'abbr', 'links']

    def get_links(self, obj):
        return {
            "self": f"{SITE_URL}/teams/{obj.id}/",
            "roster": f"{SITE_URL}/teams/{obj.id}/roster/",
            "games": f"{SITE_URL}/teams/{obj.id}/games/",
        }


class PlayerSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    links = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = [
            'id', 
            'name', 
            'position', 
            'jersey', 
            'team', 
            'country', 
            'school', 
            'birthdate',
            'height',
            'weight', 
            'links',
        ]
        ordering = ["team__team_name"]

    def get_links(self, obj):
        return {
            "self": f'{SITE_URL}/players/{obj.id}/', 
            "stats": f'{SITE_URL}/player-stats/{obj.id}/'
        }


class PlayerStatSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)

    # calculated field AVGs
    mpg = serializers.ReadOnlyField()
    ppg = serializers.ReadOnlyField()
    apg = serializers.ReadOnlyField()
    rpg = serializers.ReadOnlyField()
    stl_pg = serializers.ReadOnlyField()
    blk_pg = serializers.ReadOnlyField()
    tov_pg = serializers.ReadOnlyField()

    class Meta:
        model = PlayerStat
        fields = [
            'player', 
            'season', 
            'stat_type',
            'updated_at', 
            'gmp',
            'mpg',
            'ppg',
            'apg',
            'rpg',
            'stl_pg',
            'blk_pg',
            'tov_pg',
        ]


class TeamStatSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    
    # calculated field AVGs
    ppg = serializers.ReadOnlyField()

    class Meta:
        model = TeamStat
        fields = [
            'id', 
            'team', 
            'season', 
            'stat_type', 
            'wins', 
            'losses', 
            'ppg'
        ]