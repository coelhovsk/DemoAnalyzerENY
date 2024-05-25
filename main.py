import os
from demoparser2 import DemoParser


class DemoC:
    def __init__(self, filepath):
        self.demo = DemoParser(filepath)  # starting variables

    def data_frame_to_excel(self):
        self.demo = DemoParser("inferno.dem")  # parsing the demo with the path of the .dem file

        # file output directory a
        output_directory = r"path"

        # verify that the directory exists
        os.makedirs(output_directory, exist_ok=True)

        # list of available events
        event_list = ['player_activate', 'hegrenade_detonate', 'round_time_warning', 'bomb_planted',
                      'item_pickup_slerp',
                      'server_cvar', 'flashbang_detonate', 'player_ping', 'cs_intermission', 'cs_win_panel_match',
                      'player_sound', 'inferno_expire', 'player_connect', 'switch_team', 'player_connect_full',
                      'player_ping_stop', 'cs_round_start_beep', 'bomb_exploded', 'player_team', 'begin_new_match',
                      'weapon_fire', 'cs_round_final_beep', 'hltv_fixed', 'player_death', 'item_pickup',
                      'announce_phase_end',
                      'vote_cast', 'round_announce_match_point', 'round_announce_last_round_half', 'bomb_defused',
                      'round_announce_match_start', 'round_end_upload_stats', 'player_spawn', 'decoy_detonate',
                      'hltv_versioninfo', 'round_officially_ended', 'player_disconnect', 'decoy_started',
                      'smokegrenade_detonate', 'bomb_dropped', 'player_given_c4', 'bomb_pickup', 'inferno_startburn',
                      'round_freeze_end', 'hltv_chase', 'entity_killed', 'cs_pre_restart', 'player_hurt',
                      'smokegrenade_expired']

        for event in event_list:
            try:
                # Parse the event (return a DataFrame)
                parsed_event = self.demo.parse_event(event)

                # defining file output
                output_file = os.path.join(output_directory, f"{event}.xlsx")

                # saving the dataframe in excel format
                parsed_event.to_excel(output_file, index=False)

                print(f"Saved {event} to {output_file}")
            except Exception as e:
                print(f"An error occurred while processing {event}: {e}")

    def start_round(self):
        freezetime_end = self.demo.parse_event("round_freeze_end") # parsing round freeze ticks
        freezetime_end_ticks = [] # creating a list variable that will receive the ticks 
        for tick in range(len(freezetime_end)):
            freezetime_end_ticks.append(freezetime_end["tick"][tick]) # adding ticks values to list
        return freezetime_end_ticks # returning the list

    def end_round(self):
        round_ended = self.demo.parse_event("round_officially_ended") # parsing round end ticks
        round_ended_ticks = [] # creating a list variable that will receive the ticks 
        for tick in range(len(round_ended)):
            if round_ended["tick"][tick] not in round_ended_ticks: # filtering duplicated values
                round_ended_ticks.append(round_ended["tick"][tick]) # adding the unique tick to the list
        return round_ended_ticks # returning the list


demo = DemoC("inferno.dem") 

startR_ticks = demo.start_round()
endR_ticks = demo.end_round()

print(f"====================\nSTART TICKS: \n{startR_ticks}\n====================\nEND TICKS:\n{endR_ticks}")
