from api.utils import get_team_roster, get_team_ids
from celery import shared_task
import time
import pandas as pd




@shared_task
def add(x, y):
    return x + y

@shared_task
def roster_to_csv():
    all_rosters = []
    

    for team_id in get_team_ids():
        try:
            print(f"Fetching roster for team_id={team_id}...")
            roster = get_team_roster(team_id=str(team_id))

            roster_df = pd.DataFrame(roster)
            roster_df.to_csv(f"./sheets/teams/rosters/{team_id}.csv", index=False)
            # all_rosters.extend(roster)
            time.sleep(1.2)  # be polite to the API
        except Exception as e:
            print(f"Failed for team_id={team_id}: {e}")


    print("Saved rosters.csv")

