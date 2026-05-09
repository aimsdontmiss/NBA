from django.db.models import Q

from api.models import Player
from games.models import Game


class TeamSelector:

    @staticmethod
    def roster(team_id):

        return (
            Player.objects
            .filter(
                team_id=team_id,
                active=True
            )
            .exclude(jersey__isnull=True)
            .select_related("team")
        )

    @staticmethod
    def games(team):

        return (
            Game.objects
            .filter(
                Q(home_team=team) |
                Q(away_team=team)
            )
            .select_related(
                "home_team",
                "away_team",
                "victor"
            )
            .order_by("date")
        )