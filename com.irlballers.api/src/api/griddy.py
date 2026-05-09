import os
import time
import django
from django.core.management.base import BaseCommand
from django.db import transaction
from nba_api.stats.endpoints import CommonPlayerInfo, PlayerCareerStats, CommonTeamRoster, LeadersTiles, LeagueLeaders
from nba_api.stats.library.parameters import SeasonAll
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

from requests import ReadTimeout, RequestException




os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
django.setup()


def get_team_roster(team_id, retries=3):
    for attempt in range(1, retries + 1):
        try:
            return CommonTeamRoster(
                team_id=team_id,
                timeout=60
            ).get_normalized_dict()["CommonTeamRoster"]

        except ReadTimeout:
            print(f"Timeout for team {team_id}, attempt {attempt}/{retries}")
            time.sleep(2 * attempt)

        except RequestException as e:
            print(f"Request failed for team {team_id}: {e}")
            return None

    return None




def main():
    
    team_ids = pd.read_csv("./sheets/teams/teams.csv")['id'].tolist()

    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     results = list(executor.map(get_team_roster, team_ids))

    # for roster in results:
    #     pd.DataFrame(roster).to_csv(f"./sheets/teams/rosters/{roster[0]['TeamID']}.csv", index=False)
    #     print(roster)


    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(get_team_roster, team_id): team_id
            for team_id in team_ids
        }

        for future in as_completed(futures):
            team_id = futures[future]

            try:
                roster = future.result()
            except Exception as e:
                print(f"Unexpected error for team {team_id}: {e}")
                continue

            if not roster:
                print(f"Skipped team {team_id}")
                continue

            pd.DataFrame(roster).to_csv(
                f"./sheets/teams/rosters/{team_id}.csv",
                index=False
            )

            print(f"Saved roster for team {team_id}")


if __name__ == "__main__":
    main()