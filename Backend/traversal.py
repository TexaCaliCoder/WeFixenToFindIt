import requests
import random
from datetime import datetime, timedelta
import time
from util import follow_path, shortest_path_to, nearest_open_path, Queue
from getters import get_room_dict, get_current_room, get_user
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
    room_info = get_current_room(header_info)
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
    items_onboard = []

    while rooms_to_visit:

        purpose = "move randomly"

        # ITEM LOOKUP
        def item_lookup():
            while True:
                room_info = get_current_room(header_info)
                if len(room_info['items']) == 0:
                    print('there is nothing left here')
                    return

                user = get_user(header_info)

                item = room_info['items'][0]
                item_name = {"name": item}
                pickup = requests.post(
                    'https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/', headers=header_info, json=item_name).json()
                time.sleep(pickup['cooldown'])
                print("there is a", pickup['name'])
                if pickup['weight'] + user['encumbrance'] <= user['strength']:
                    items_onboard.append(pickup['name'])
                    item_get(pickup['name'])
                else:
                    shop_path = shortest_path_to(shop, room_info['room_id'])
                    follow_path(room_info['room_id'],
                                shop_path['path'], header_info)
                    print('going to sell goods')
                    sell_items()
                    return

        # ITEM GET
        def item_get(item_to_get):
            received_item = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/take/',
                                          headers=header_info, json={"name": item_to_get}).json()
            time.sleep(received_item['cooldown'])
            print('picked up the', item_to_get)
            return

        def sell_items():
            while True:
                confirm = 'no'
                item_to_sell = ""
                if len(items_onboard) == 0:
                    return
                elif confirm == "no":
                    item_to_sell = items_onboard.pop()
                    sale = {"name": item_to_sell}
                    confirm = "yes"
                else:
                    sale = {"name": item_to_sell, "confirm": "yes"}
                    confirm = 'no'
                merchant = requests.post(
                    "https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/", headers=header_info, json=sale).json()
                time.sleep(merchant['cooldown'])
                print('sold the', item_to_sell, merchant["messages"])

        while purpose == "move randomly":
            rooms_we_have = get_room_dict()
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
                'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=header_info, json=db_send).json()
            print("moved to", new_room['room_id'])
            time.sleep(new_room['cooldown'])
            room_info = dict(new_room)
            if next_room == -1:
                add_new_room(c_rm['room_id'], new_room['room_id'], {
                }, move, direction_possibilities[move], False)
            purpose = "item lookup"
            item_lookup()

        # DIRECTION DECISION TREE
        # check timer again
        while purpose == 'move purposefully':
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
                purpose = 'move randomly'
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
