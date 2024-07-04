from awpy import Demo
import pandas as pd
pd.set_option('display.max_columns', None)
class collectingClutches:
    def __init__(self, filepath):
        self.demo = Demo(filepath)

    def get_clutches(self):
        # collecting dataframes from awpy
        deaths = self.demo.kills[["tick", "victim_steamid", "victim_name", "victim_team_name", "victim_team_clan_name"]]
        rounds = self.demo.rounds[["round", "start", "end", "winner", "reason"]]
        teams = self.demo.ticks[["team_clan_name", "name", "steamid"]]

        # initializing  dataframes
        df_deaths = pd.DataFrame(deaths)
        df_rounds = pd.DataFrame(rounds)
        df_teams = pd.DataFrame(teams)

        # storing unique name players and their team name
        dt_teams = df_teams.drop_duplicates('name').sort_values('team_clan_name').reset_index(drop=True)
        team_names = dt_teams['team_clan_name'].unique()

        # initializing global variables
        results = []
        structured_data = []
        tick_end_clutch = None

        # iterating for each round
        for _, round_row in df_rounds.iterrows():
            round_x = round_row["round"]
            start_tick = round_row['start']
            end_tick = round_row['end']
            round_winner = round_row['winner']
            win_reason = round_row['reason']

            # storing kills per round
            deaths_in_round = df_deaths[(df_deaths['tick'] >= start_tick) & (df_deaths['tick'] <= end_tick)]
            deaths_in_round = deaths_in_round.copy()
            deaths_in_round['round'] = round_x
            results.append(deaths_in_round)
            df_death_round = pd.concat(results).reset_index(drop=True).sort_values('tick')

            # initializing a dictionary to store the team side
            team_sides = {
                team_names[0]: None,
                team_names[1]: None
            }

            # taking the first values that contain the team side
            first_team_rows = df_deaths.groupby('victim_team_clan_name').first().reset_index()
            first_team_rows = first_team_rows.to_dict('records')
            for row in first_team_rows:
                team_name = row['victim_team_clan_name']
                team_side = row['victim_team_name']

                if team_name in team_sides: # transforming TERRORIST to T
                    team_sides[team_name] = 'T' if team_side == 'TERRORIST' else 'CT'

            # switch the side from CT to T or T to CT
            if round_x >= 13:
                if team_sides[team_names[0]] == 'CT':
                    team_sides[team_names[0]] = 'T'
                    team_sides[team_names[1]] = 'CT'
                elif team_sides[team_names[0]] == 'T':
                    team_sides[team_names[0]] = 'CT'
                    team_sides[team_names[1]] = 'T'

            # separating all players by team
            team1_players = dt_teams[dt_teams['team_clan_name'] == team_names[0]]['name'].tolist()
            team2_players = dt_teams[dt_teams['team_clan_name'] == team_names[1]]['name'].tolist()
            players_alive = {
                "pa_team1": team1_players[:],
                "pa_team2": team2_players[:]
            }

            # iterating for each kill in round
            df_death_round_current = df_death_round[df_death_round['round'] == round_x]
            for _, deathround_row in df_death_round_current.iterrows():
                victimName = deathround_row['victim_name']
                tick_end_clutch = deathround_row['tick']

                # removing the dead player from players_alive
                if victimName in players_alive['pa_team1']:
                    players_alive["pa_team1"].remove(victimName)
                elif victimName in players_alive['pa_team2']:
                    players_alive["pa_team2"].remove(victimName)

            # check if there is one alive player and if they won
            if len(players_alive["pa_team1"]) == 1 and len(players_alive["pa_team2"]) == 0:
                if round_winner == team_sides[team_names[0]]:
                    player = players_alive["pa_team1"][0]
                    condition = '1'
                    playerSID1 = dt_teams.loc[dt_teams['name'] == player, 'steamid'].reset_index(drop=True).iloc[0]
                    structured_data.append([player, round_x, tick_end_clutch, condition, win_reason, playerSID1])
                else:
                    player = players_alive["pa_team1"][0]
                    condition = '0'
                    playerSID1 = dt_teams.loc[dt_teams['name'] == player, 'steamid'].reset_index(drop=True).iloc[0]
                    structured_data.append([player, round_x, tick_end_clutch, condition, win_reason, playerSID1])

            elif len(players_alive["pa_team2"]) == 1 and len(players_alive["pa_team1"]) == 0:
                if round_winner == team_sides[team_names[1]]:
                    player = players_alive["pa_team2"][0]
                    condition = '1'
                    playerSID2 = dt_teams.loc[dt_teams['name'] == player, 'steamid'].reset_index(drop=True).iloc[0]
                    structured_data.append([player, round_x, tick_end_clutch, condition, win_reason, playerSID2])
                else:
                    player = players_alive["pa_team2"][0]
                    condition = '0'
                    playerSID2 = dt_teams.loc[dt_teams['name'] == player, 'steamid'].reset_index(drop=True).iloc[0]
                    structured_data.append([player, round_x, tick_end_clutch, condition, win_reason, playerSID2])

        # storing clutches in the df, and then, returning
        df_clutch_data = pd.DataFrame(structured_data, columns=['name', 'round', 'tick_end_clutch', 'condition', 'win_reason', 'steam_ID'])
        return df_clutch_data

demo = collectingClutches('vitality-vs-faze-m1-nuke.dem')
clutches = demo.get_clutches()