import requests
import sys
from util import shortest_path_to, follow_path, header_info, Queue
from getters import get_current_room

start = 495

shop = 1
pirate_ry = 467
flying_shrine = 22
ghost_shrine = 499
speed_shrine = 461
mine = 250
transmog = 495

if len(sys.argv) == 1:
    print("Please include a room to travel to")
    exit()

dest = int(sys.argv[1])
start = get_current_room()['room_id']

path = shortest_path_to(dest, start)

follow_path(start, path['path'], header_info)


