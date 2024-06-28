from awpy import Demo
from pathlib import Path
from analyzes import position_analysis, visualization

demo_archive = Path('path')
map_image_archive = Path('path')
parser = Demo(demo_archive)

player_positions = position_analysis.get_players_position(parser)
# visualization.animate_player_positions(player_positions, map_image_archive)
