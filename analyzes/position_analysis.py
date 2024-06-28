import pandas as pd


def get_players_position(parser):
    ticks = parser.ticks
    player_positions = ticks[["X", "Y", "tick", "steamid", "name"]]
    return player_positions
