from django.db import models
from api.models import *


# Create your models here.

class Game(models.Model):
    id         = models.CharField(max_length=20, primary_key=True)
    date       = models.DateField()
    home_team  = models.ForeignKey(
                        Team, on_delete=models.CASCADE, 
                        related_name="home_team"
                    )
    away_team  = models.ForeignKey(
                        Team, on_delete=models.CASCADE, 
                        related_name="away_team"
                    )
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    played     = models.BooleanField(default=False)
    victor     = models.ForeignKey(
                        Team, on_delete=models.CASCADE, 
                        blank=True, 
                        null=True, 
                        related_name="victor"
                    )
    
    class Meta:
        indexes = [
            models.Index(fields=["home_team", "-date"]),
            models.Index(fields=["away_team", "-date"]),
        ]

    def __str__(self):
        return f"{self.away_team} at {self.home_team} on {self.date}"
    

class Record(models.Model):
    team        = models.ForeignKey(Team, on_delete=models.CASCADE)
    wins        = models.IntegerField(default=0)
    losses      = models.IntegerField(default=0)
              
    home_wins   = models.IntegerField(default=0)
    road_wins   = models.IntegerField(default=0)
    
    home_losses = models.IntegerField(default=0)
    road_losses = models.IntegerField(default=0)

    conf_rank   = models.IntegerField(blank=True, null=True)
    div_rank    = models.IntegerField(blank=True, null=True)

    @property
    def games_played(self):
        return self.wins + self.losses

    @property
    def win_pct(self):
        total = self.games_played
        return round(self.wins / total, 3) if total else 0.0

    # simple method to update record based on game result
    def apply_dub(self, home: bool, won: bool):
        if won:
            self.wins += 1
            if home:
                self.home_wins += 1
            else:
                self.road_wins += 1
        else:
            self.losses += 1
            if home:
                self.home_losses += 1
            else:
                self.road_losses += 1
        self.save()

    def __str__(self):
        return f"{self.team}: {self.wins}-{self.losses}"