import requests
import random
from datetime import datetime, timedelta
import time
from util import follow_path, shortest_path_to, nearest_open_path, Queue
from getters import get_room_dict, get_current_room, get_user, item_get
from setters import add_new_room, closed_exits

shop = 1
pirate_ry = 467
flying_shrine = 22
ghost_shrine = 499
speed_shrine = 461

# "Token dccec1ad173d2abaf88b542a02095f8d93ea97df",
# "Token 8271c9035b3a113a16111392722a7bb4d9278a2c",
# "Token 64936db353e36faa7ec880bb81331706cd4216a7",
# "Token 508711f53445fa67d8bdc1c97da256eacaef2e5e"
api_key = "Token 508711f53445fa67d8bdc1c97da256eacaef2e5e"
header_info = {'Authorization': api_key}


def traversal():
    rooms_we_have = get_room_dict()
    room_info = get_current_room()
    if room_info['room_id'] not in rooms_we_have:
        db_send = {
            "id": room_info["room_id"],
            "coordinates": room_info["coordinates"],
            "name": room_info["title"],
            "description": room_info["description"],
        }
        requests.post("https://wegunnagetit.herokuapp.com/rooms/",
                      json=db_send).json()

    rooms_to_visit = True

    while rooms_to_visit:
    
        visited_rooms = get_room_dict()

        if room_info['room_id'] not in visited_rooms:
            db_send = {
                "id": room_info["room_id"],
                "coordinates": room_info["coordinates"],
                "name": room_info["title"],
                "description": room_info["description"],
            }
            requests.post(
                "https://wegunnagetit.herokuapp.com/rooms/", json=db_send).json()
            visited_rooms = get_room_dict()

        c_rm = room_info
        c_rm_n = True if 'n' in room_info['exits'] and visited_rooms[c_rm['room_id']
                                                                        ]['n'] == -1 else False
        c_rm_s = True if 's' in room_info['exits'] and visited_rooms[c_rm['room_id']
                                                                        ]['s'] == -1 else False
        c_rm_e = True if 'e' in room_info['exits'] and visited_rooms[c_rm['room_id']
                                                                        ]['e'] == -1 else False
        c_rm_w = True if 'w' in room_info['exits'] and visited_rooms[c_rm['room_id']
                                                                        ]['w'] == -1 else False

        if c_rm_n:
            old_room = c_rm['room_id']
            new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/',
                                        headers=header_info, json={"direction": "n"}).json()
            time.sleep(new_room['cooldown'])
            db_send = {
                "id": new_room["room_id"],
                "coordinates": new_room["coordinates"],
                "name": new_room["title"],
                "description": new_room["description"],
            }
            # post new room to db and change directions of new room and old room to reflect new info
            if new_room['room_id'] not in visited_rooms:
                add_new_room(
                    old_room, new_room['room_id'], db_send, "n", "s", True)
            else:
                add_new_room(
                    old_room, new_room['room_id'], db_send, "n", "s", False)
            closed_exits(new_room)
            room_info = dict(new_room)
        elif c_rm_e:
            old_room = c_rm['room_id']
            new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/',
                                        headers=header_info, json={"direction": "e"}).json()
            time.sleep(new_room['cooldown'])
            db_send = {
                "id": new_room["room_id"],
                "coordinates": new_room["coordinates"],
                "name": new_room["title"],
                "description": new_room["description"],
            }
            # post new room to db and change directions of new room and old room to reflect new info
            if new_room['room_id'] not in visited_rooms:
                add_new_room(
                    old_room, new_room['room_id'], db_send, "e", "w", True)
            else:
                add_new_room(
                    old_room, new_room['room_id'], db_send, "e", "w", False)
            closed_exits(new_room)
            room_info = dict(new_room)
        elif c_rm_s:
            old_room = c_rm['room_id']
            new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/',
                                        headers=header_info, json={"direction": "s"}).json()
            time.sleep(new_room['cooldown'])
            db_send = {
                "id": new_room["room_id"],
                "coordinates": new_room["coordinates"],
                "name": new_room["title"],
                "description": new_room["description"],
            }
            # post new room to db and change directions of new room and old room to reflect new info
            if new_room['room_id'] not in visited_rooms:
                add_new_room(
                    old_room, new_room['room_id'], db_send, "s", "n", True)
            else:
                add_new_room(
                    old_room, new_room['room_id'], db_send, "s", "n", False)
            closed_exits(new_room)
            room_info = dict(new_room)
        elif c_rm_w:
            old_room = c_rm['room_id']
            new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/',
                                        headers=header_info, json={"direction": "w"}).json()
            time.sleep(new_room['cooldown'])
            db_send = {
                "id": new_room["room_id"],
                "coordinates": new_room["coordinates"],
                "name": new_room["title"],
                "description": new_room["description"],
            }
            # post new room to db and change directions of new room and old room to reflect new info
            if new_room['room_id'] not in visited_rooms:
                add_new_room(
                    old_room, new_room['room_id'], db_send, "w", "e", True)
            else:
                add_new_room(
                    old_room, new_room['room_id'], db_send, "w", "e", False)

            closed_exits(new_room)
            room_info = dict(new_room)
        elif len(visited_rooms) >= 500:
            print("we're done here")
            rooms_to_visit = False
        else:
            print('going to find a new way around from room #',
                    c_rm['room_id'])
            last_open = nearest_open_path(c_rm["room_id"])
            room_info = follow_path(
                c_rm["room_id"], last_open["path"], header_info)


def go_shopping(start):
    shop_path = shortest_path_to(shop, start)
    follow_path(start, shop_path['path'], header_info)
    # TODO go_shopping
    # get user info
    # while there are items
    # if the timer is up
    # pop an item off
    # sell an item
    # go back to starting room and randomly move

# TODO go to a shrine
# TODO set check for 1000 gold and travel to Pirate Ry

# traversal()
