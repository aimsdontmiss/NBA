import nba_api.stats.endpoints.playbyplayv3
import nba_api.stats.endpoints.leaguedashlineups



game_id ='0022501108'

def get_play_by_play(game_id):
    pbp = nba_api.stats.endpoints.playbyplayv3.PlayByPlayV3(game_id=game_id)
    return pbp.get_data_frames()[0]

play_by_play_data = get_play_by_play(game_id)

print(play_by_play_data.head())
print(play_by_play_data.columns)

def get_lineups(game_id):
    lineups = nba_api.stats.endpoints.leaguedashlineups.LeagueDashLineups(season='2023-24', season_type_all_star='Regular Season')
    return lineups.get_data_frames()[0]

lineups_data = get_lineups(game_id)
print(lineups_data.head())
print(lineups_data.columns)