from django.db import transaction
from api.utils import get_player, get_team_ids, to_int
from api.models import *
import pandas as pd
import time
from django.db import transaction
from django.core.management.base import BaseCommand

RATE_LIM = 0.6
BATCH_SIZE = 50

@transaction.atomic()
def update_status():

    batch_size = 50
    batch = []

    players = Player.objects.all()

    for player in players:
        info = get_player(player.id)
        
        if info.get("ROSTERSTATUS") == "Active": 
            player.active = True
        else:
             player.active = False

        batch.append(player)

        if len(batch) >= batch_size:
            Player.objects.bulk_update(batch, ["active"])
            batch.clear()

        time.sleep(0.3)  # keep your rate limit
        print(player)

    if batch:
        Player.objects.bulk_update(batch, [ "active" ])




@transaction.atomic()
def clean_players():
    batch_size = 50
    batch = []

    players = Player.objects.all()

    for player in players:
        info = get_player(player.id)
        
        player.country = info.get("COUNTRY")
        player.jersey = to_int(info.get("JERSEY"))
        
        if info.get("ROSTERSTATUS") == "Active": 
            player.active = True
        else:
             player.active = False

        batch.append(player)

        if len(batch) >= batch_size:
            Player.objects.bulk_update(batch, ["country", "jersey", "active" ])
            batch.clear()

        time.sleep(0.6)  # keep your rate limit
        print(player)

    if batch:
        Player.objects.bulk_update(batch, [ "country", "jersey", "active" ])


class Command(BaseCommand):
    help = "Supplement (clean) Player objects"

    def handle(self, *args, **kwargs):
            clean_players()
            # update_status()

            for player in Player.objects.all():
                print(f"{ player.name } (#{ player.jersey }) from { player.country } active: { player.active } on { player.team }")
                # print(f"{ player.name } isAcvtive: { player.active } on { player.team }")





    

        
