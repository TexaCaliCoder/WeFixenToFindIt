import requests
from util import shortest_path_to, follow_path, header_info, Queue

start = 495

shop = 1
pirate_ry = 467
flying_shrine = 22
ghost_shrine = 499
speed_shrine = 461
mine = 250
transmog = 495

path = shortest_path_to(mine, start)

follow_path(start, path['path'], header_info)


