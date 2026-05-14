import os
import django
from django.core.management.base import BaseCommand
from django.db import transaction
from nba_api.stats.endpoints import CommonPlayerInfo, PlayerCareerStats, CommonTeamRoster, LeadersTiles, LeagueLeaders
from nba_api.stats.library.parameters import SeasonAll
import pandas as pd
from api.models import PlayerStat
from api.utils import leaders_to_csv, pop_player_stats



class Command(BaseCommand):
    help = "Populate player stats data"

    def handle(self, *args, **kwargs):
        leaders_to_csv()
        pop_player_stats()

        for stat in PlayerStat.objects.all():
            print(f"{stat.player.name} had {stat.ppg} ppg in the {stat.season} season")