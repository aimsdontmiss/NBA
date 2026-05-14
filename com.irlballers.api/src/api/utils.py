import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
django.setup()

# from api.models import Player, Team

from nba_api.stats.endpoints import CommonPlayerInfo, CommonTeamRoster, LeadersTiles, LeagueLeaders, PlayerCareerStats
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.static import teams 
import pandas as pd
import time
from .models import *
from django.db import transaction
from urllib.request import Request, urlopen
import json





def get_player(player_id):
    info = CommonPlayerInfo(player_id=player_id).get_normalized_dict()
    return info["CommonPlayerInfo"][0]


def get_player_stats(player_id):
    stats = PlayerCareerStats(player_id=player_id).get_normalized_dict()
    return stats["SeasonTotalsRegularSeason"][-1] # the -1 index get the most recent szn


def get_team_roster(team_id):
    roster = CommonTeamRoster(team_id=team_id).get_normalized_dict()
    return roster["CommonTeamRoster"]


def get_leader_teams():
    leaders = LeadersTiles().get_normalized_dict()
    return leaders["LeadersTiles"]


def get_league_leaders():
    leaders = LeagueLeaders().get_normalized_dict()
    return leaders["LeagueLeaders"]


def get_all_teams():
    teams = CommonTeamRoster().get_normalized_dict()
    return teams["CommonTeamRoster"]


def teams_to_csv():
    raw_teams = teams._get_teams()
    teams_df = pd.DataFrame(raw_teams)
    print(teams_df.head())
    teams_df.to_csv("./sheets/teams.csv", index=False)


def get_teams_list():
    teams_df = pd.read_csv("./sheets/teams/teams.csv")
    return [
        {'TEAM_NAME': team['nickname'], 'TEAM_ID': team['id']} for team in teams_df.to_dict(orient='records')
    ]


def get_team_ids():
    # pass
    teams_list = get_teams_list()
    teams = [ team['TEAM_ID'] for team in teams_list ]
    return teams


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


def leaders_to_csv():
    leaders = get_league_leaders()
    leaders_df = pd.DataFrame(leaders)
    print(leaders_df.head())
    leaders_df.to_csv("./sheets/players/league_leaders.csv", index=False)
    print("Saved league_leaders.csv")
    


def get_schedule():
    # nba_api schedule url ref.(in json):
    # https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2025/league/00_full_schedule.json 
    
    try:
        req = Request(
            "https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2025/league/00_full_schedule.json",
            headers={"User-Agent": "Mozilla/5.0"},
        )

        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())

        month_order = {
            'october': 1,
            'november': 2,
            'december': 3,
            'january': 4,
            'february': 5,
            'march': 6,
            'april': 7,
        }

        # sort the list of months based on their order in the month_order dictionary
        # data[0]['mscd']
        # print(l1[0]['mscd'])
        games = []

        sorted_months = sorted(
            data["lscd"],
            key=lambda m: month_order[m["mscd"]["mon"].lower()]
        )
        for month in sorted_months:
            for game in month["mscd"]["g"]:
                games.append({
                    "game_id": game["gid"],
                    "game_code": game["gcode"],
                    "date": game["gdte"],
                    "home_team_id": game["h"]["tid"],
                    "home_team": game["h"]["ta"],
                    "away_team_id": game["v"]["tid"],
                    "away_team": game["v"]["ta"],
                    "arena": game["an"],
                    "city": game["ac"],
                    "state": game["as"],
                    "status_text": game["stt"],
                })
            # games.sort(key=lambda month: month_order[month['mscd']['month']])
        df = pd.DataFrame(games)
        sheet = df.to_csv("./sheets/lscd.csv", index=False)
        print(df.head())
        print(f"Total games: {len(df)}")

    except Exception as e:
        print(f"Error occurred: {e}")


def pop_teams():
    teams_df = pd.read_csv("./sheets/teams/teams.csv").to_dict(orient='records')

    for team in teams_df:
        if not Team.objects.filter(id=team['id']).exists():
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


def pop_players():
    id_list = get_team_ids()

    # populate the database with Player instances
    for team_id in id_list:
        roster_df = pd.read_csv(f"./sheets/teams/rosters/{team_id}.csv")
        for player in roster_df.to_dict(orient='records'):
            print(player)
            if not Player.objects.filter(id=player['PLAYER_ID']).exists():
                common_info = get_player(player['PLAYER_ID'])
                print(common_info)
                slug_name = player.get('PLAYER_SLUG') or common_info.get('PLAYER_SLUG') or None
                player_instance = Player(
                    id=player['PLAYER_ID'],
                    name=player['PLAYER'],
                    slug_name=slug_name,
                    team_id=int(player['TeamID']),
                    country=common_info.get('COUNTRY', None),
                    school=common_info.get('SCHOOL', None),
                    birthdate=common_info.get('BIRTHDATE', None),
                    height=common_info.get('HEIGHT') or None,
                    weight=to_int(common_info.get('WEIGHT')),
                    position=common_info.get('POSITION', None),
                    jersey=to_int(player['NUM']),
                    active=True
                )
                player_instance.save()
                print(f"Created player {player['PLAYER']}")
                time.sleep(1.2)  # API ettiquette


def pop_player_stats():
    leaders = pd.read_csv("./sheets/players/league_leaders.csv").to_dict(orient='records')

    for player in leaders:
        if Player.objects.filter(id=player['PLAYER_ID']).exists():
            stat = PlayerStat(
                player    = Player.objects.get(id=player['PLAYER_ID']),
                pts       = player['PTS'],
                reb  = player['REB'],
                dreb = player['DREB'],
                oreb = player['OREB'],
                ast   = player['AST'],
                stl    = player['STL'],
                blk    = player['BLK'],
                tov = player['TOV'],
                fgm    = player['FGM'],
                fga   = player['FGA'],
                ftm   = player['FTM'],
                fta   = player['FTA'],
                tpm   = player['FG3M'],
                tpa   = player['FG3A'],
                season = '2025-26',
                stat_type = PlayerStat.STAT_TYPES[0][0], # regular season
                team = Team.objects.get(id=player['TEAM_ID']),
                pf = player['PF'],
                gmp = player['GP'],
                mins = player['MIN'],
                updated_at = time.time(),
            )
            stat.save()
            print(f"Created stats for player {player['PLAYER']}")
            time.sleep(.2)  # API ettiquette


def pop_team_stats():
    pass


# making our player models based on our csv sheets
def to_int(value):
    if value in (None, '', ' ', 'None'):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None



@transaction.atomic
def main():
    # roster_to_csv()

    # populate teams
    # pop_teams()

    # populate players
    # pop_players()

    # populate player stats
    # leaders_to_csv()
    pop_player_stats()

    # get schedule
    # get_schedule()



if __name__ == "__main__":
    main()