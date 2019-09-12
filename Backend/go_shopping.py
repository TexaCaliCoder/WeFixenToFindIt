import sys
import requests
import time
import random
import util
import getters
from setters import add_new_room, closed_exits

def shopping(money_to_earn):
    coins = 0
    room_info = getters.get_current_room()
    while int(money_to_earn) > coins:
        rooms_we_have = getters.get_room_dict()
        possible_moves = []
        c_rm = room_info
        direction_possibilities = {
            'n': 's',
            's': 'n',
            'e': 'w',
            'w': 'e'
        }
        c_rm_n = True if 'n' in room_info['exits'] else False
        c_rm_s = True if 's' in room_info['exits'] else False
        c_rm_e = True if 'e' in room_info['exits'] else False
        c_rm_w = True if 'w' in room_info['exits'] else False
        if c_rm_n:
            possible_moves.append("n")
        if c_rm_s:
            possible_moves.append("s")
        if c_rm_e:
            possible_moves.append("e")
        if c_rm_w:
            possible_moves.append("w")
        move = random.choice(possible_moves)

        next_room = rooms_we_have[c_rm['room_id']][move]
        db_send = {"direction": move, "next_room_id": str(
            next_room)} if next_room > -1 else {"direction": move}
        new_room = requests.post(
            util.room_db + 'move/', headers=util.header_info, json=db_send).json()
        print("moved to", new_room['room_id'])
        time.sleep(new_room['cooldown'])
        room_info = dict(new_room)
        if next_room == -1:
            add_new_room(c_rm['room_id'], new_room['room_id'], {
            }, move, direction_possibilities[move], False)
        getters.item_lookup()


money_to_earn = sys.argv[1]

shopping(money_to_earn)

print("You have the money now")
