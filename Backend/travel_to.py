import requests
from traversal import Queue, get_room_dict, shortest_path_to, follow_path

start = 461

shop = 1
pirate_ry = 467
flying_shrine = 22
ghost_shrine = 499
speed_shrine = 461

path = shortest_path_to(flying_shrine, start)

follow_path(start, path['path'])


