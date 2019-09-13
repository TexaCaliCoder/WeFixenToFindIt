import sys
import util
import travel_to
from getters import get_current_room

if len(sys.argv) == 1:
    print("Please include a number of coins to mine")
    exit()

coins = int(sys.argv[1])
start = get_current_room()['room_id']
