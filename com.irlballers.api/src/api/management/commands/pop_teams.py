import pandas as pd
from django.db import transaction
from api.models import Team
from django.core.management.base import BaseCommand


@transaction.atomic
def pop_teams():
    teams_df = pd.read_csv("./sheets/teams/teams.csv").to_dict(orient='records')
    for team in teams_df: 
        try:      
            team_instance = Team(
                id=team['id'],
                city_name=team['city'],
                team_name=team['nickname'],
                abbr=team['abbreviation'],
                conf=None,  # API doesn't provide conference info in this endpoint
                arena=None,  # API doesn't provide arena info in this endpoint
            )
            team_instance.save()
            print(f"Created team {team['nickname']}")
        except Exception as e:
            print(f"Error occurred: {e}")




class Command(BaseCommand):
    help = "Populate and clean game data"

    def handle(self, *args, **kwargs):
        pop_teams()
        
        for team in Team.objects.all():
            print(f"{team.team_name} from {team.city_name}")