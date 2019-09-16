import requests

import util

# This function adds room information into the database
def add_new_room(old, new, db_send, dir_trav, opp_dir_trav, room_bool):
    if old != new:
        if room_bool:
            requests.post(util.storage, json=db_send).json()
            print('added room', new)
        requests.put(util.storage + str(old) + '/', json={dir_trav: new}).json()
        requests.put(util.storage + str(new) + '/', json={opp_dir_trav: old}).json()
        print('changed room directions', new, '&', old)


def closed_exits(room):
    r_id = str(room['room_id'])
    exits = room['exits']
    dirs = ['n', 's', 'e', 'w']
    for door in dirs:
        if door not in exits:
            requests.put(util.storage + r_id + '/', json={door: -100})