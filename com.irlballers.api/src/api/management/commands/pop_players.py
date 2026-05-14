import time
from api.utils import to_int
from api.utils import get_team_ids, get_team_roster, get_player
from api.models import Player
import pandas as pd
from django.db import transaction
from django.core.management.base import BaseCommand
from datetime import datetime



# @transaction.atomic
# def pop_players():
#     id_list = get_team_ids()

#     # teams = []

#     # populate the database with Player instances
#     for team_id in id_list:

#         roster = []

#         roster_df = pd.read_csv(f"./sheets/teams/rosters/{team_id}.csv")
#         for player in roster_df.to_dict(orient='records'):
#             print(player)
#             if not Player.objects.filter(id=player['PLAYER_ID']).exists():
#                 common_info = get_player(player['PLAYER_ID'])
#                 print(common_info)
#                 slug_name = player.get('PLAYER_SLUG') or common_info.get('PLAYER_SLUG') or None
#                 player_instance = Player(
#                     id=player['PLAYER_ID'],
#                     name=player['PLAYER'],
#                     slug_name=slug_name,
#                     team_id=int(player['TeamID']),
#                     country=common_info.get('COUNTRY', None),
#                     school=common_info.get('SCHOOL', None),
#                     birthdate=common_info.get('BIRTHDATE', None),
#                     height=common_info.get('HEIGHT') or None,
#                     weight=to_int(common_info.get('WEIGHT')),
#                     position=common_info.get('POSITION', None),
#                     jersey=to_int(player['NUM']),
#                     active=True
#                 )
#                 roster.append(player_instance)
#                 # player_instance.save()
#                 print(f"Created player {player['PLAYER']}")
#                 time.sleep(.6)  # API ettiquette
#         Player.objects.abulk_create(roster)





def clean(value):
    return None if pd.isna(value) else value


def parse_birthdate(value):
    if pd.isna(value):
        return None
    return datetime.strptime(value, "%b %d, %Y").date()


@transaction.atomic
def pop_players():
    existing_ids = set(Player.objects.values_list("id", flat=True))

    for team_id in get_team_ids():
        roster = []
        roster_df = pd.read_csv(f"./sheets/teams/rosters/{team_id}.csv")

        for row in roster_df.to_dict(orient="records"):
            player_id = int(row["PLAYER_ID"])

            if player_id in existing_ids:
                continue

            roster.append(Player(
                id=player_id,
                name=row["PLAYER"],
                slug_name=clean(row["PLAYER_SLUG"]),
                team_id=int(row["TeamID"]),
                school=clean(row["SCHOOL"]),
                birthdate=parse_birthdate(row["BIRTH_DATE"]),
                height=clean(row["HEIGHT"]),
                weight=to_int(row["WEIGHT"]),
                position=clean(row["POSITION"]),
                jersey=to_int(row["NUM"]),
                active=None,
            ))

            existing_ids.add(player_id)

        Player.objects.bulk_create(roster)
        print(f"Created {len(roster)} players for team {team_id}")



class Command(BaseCommand):
    help = "Populate player data"

    def handle(self, *args, **kwargs):
        pop_players()

        for player in Player.objects.all():
            print(f"{player.name} from team {player.team}")