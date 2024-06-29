from awpy import Demo

class EventTracker:

    def get_kills_infos(self, playername=None):
        required_columns = [
            "tick",
            "round",

            "attacker_place",
            "attacker_X",
            "attacker_Y",
            "attacker_Z",
            "attacker_name",
            "attacker_yaw",
            "attacker_steamid",
            "attacker_side",
            "weapon",
            "hitgroup",

            "victim_X",
            "victim_Y",
            "victim_Z",
            "victim_name",
            "victim_steamid"
        ]
        round_kills = self.dem.kills[required_columns]
        if playername is not None:
            return round_kills[round_kills["attacker_name"] == playername]
        else:
            return round_kills

    def __init__(self, path):
        self.dem = Demo(path)
