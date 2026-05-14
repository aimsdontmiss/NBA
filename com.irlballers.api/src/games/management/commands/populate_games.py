from django.core.management.base import BaseCommand
from django.db import transaction
# from games.utils import pop_games, clean_games, upcoming_games
from games.models import Game
from api.models import Team
from nba_api.stats.endpoints import BoxScoreTraditionalV3
import datetime
import pandas as pd
from time import sleep


@transaction.atomic
def pop_games():
    gms = pd.read_csv(
        "./sheets/lscd.csv",
        parse_dates=["date"],
        dtype={"game_id": str},
    )

    # Load all teams once
    teams_by_id = Team.objects.in_bulk()

    games_to_create = []
    # seen_ids = set(Game.objects.values_list("id", flat=True))
    seen_ids = {str(x).zfill(10) for x in Game.objects.values_list("id", flat=True)}

    today = datetime.date.today()

    for row in gms.itertuples(index=False):
        game_id = str(row.game_id).strip().zfill(10)
        home_id = int(row.home_team_id)
        away_id = int(row.away_team_id)

        home_team = teams_by_id.get(home_id)
        away_team = teams_by_id.get(away_id)

        if not home_team or not away_team:
            print(f"Skipping {row.game_id}: missing home={home_id} away={away_id}")
            continue

        if game_id in seen_ids:
            continue

        games_to_create.append(
            Game(
                id=game_id,
                date=row.date.date(),
                home_team=home_team,
                away_team=away_team,
                played=row.date.date() < today,
            )
        )
        print(f'Game {game_id} - {away_team} at {home_team} on {row.date.date()} - {"Played" if row.date.date() < today else "Upcoming"}')


    Game.objects.bulk_create(games_to_create, batch_size=1000)
    print(f"Inserted {len(games_to_create)} games")

def get_score(game_id):
    # pass
    return BoxScoreTraditionalV3(game_id=game_id).get_data_frames()[2]

# @transaction.atomic
def clean_games():
    games = Game.objects.filter(played=True).select_related('home_team', 'away_team').order_by('date')

    missing_games = Game.objects.filter(victor__isnull=True)

    for game in missing_games:
        df = get_score(game_id=game.id)
        home = df.iloc[0]
        away = df.iloc[1]

        game.home_score = home["points"]
        game.away_score = away["points"]

        if game.home_score > game.away_score:
            winner = game.home_team
        else:
            winner = game.away_team

        game.victor = winner
        game.played = True
        game.save()
        print(f"Updated game {game.id} - Winner: {game.victor} ({game.home_score}-{game.away_score})")
        sleep(.3)  # Sleep to avoid overwhelming the API


def upcoming_games():
    return Game.objects.filter(played=False).select_related('home_team', 'away_team').order_by('date')


class Command(BaseCommand):
    help = "Populate and clean game data"

    def handle(self, *args, **kwargs):
        pop_games()
        clean_games()

        for game in upcoming_games():
            print(f"{game.away_team} at {game.home_team} on {game.date}")