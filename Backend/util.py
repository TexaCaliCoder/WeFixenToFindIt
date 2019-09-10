import requests
import random
from datetime import datetime, timedelta
import time

storage = "https://wegunnagetit.herokuapp.com/rooms/"
room_db = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
# "Token dccec1ad173d2abaf88b542a02095f8d93ea97df",
# "Token 8271c9035b3a113a16111392722a7bb4d9278a2c",
# "Token 64936db353e36faa7ec880bb81331706cd4216a7",
# "Token 508711f53445fa67d8bdc1c97da256eacaef2e5e"
api_key = "Token 508711f53445fa67d8bdc1c97da256eacaef2e5e"
header_info = {'Authorization': api_key}

# Basic Queue class


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


# Timing functions
# - takes in a number of seconds and returns the time that many seconds in the future
def countdown_setup(cooldown):
    return datetime.now() + timedelta(seconds=cooldown)


# - returns true if the time passed in is in the past
def timecheck(timer):
    if timer['time'] < datetime.now():
        return True
    else:
        return False


# These functions serve as info getters
# - retreives the list of known rooms and returns that in dictionary form
def get_room_dict():
    room_dict = {}
    room_list = requests.get(
        storage).json()
    for room in room_list:
        room_dict[room['id']] = room

    return room_dict


def get_current_room(header_info):
    room = requests.get(room_db + 'init/', headers=header_info).json()
    time.sleep(room['cooldown'])
    return room


# - retreives the current user info
def get_user(header_info): 
    user = requests.post(room_db + 'status/', headers=header_info).json()
    time.sleep(user['cooldown'])
    return user


# This function adds room information into the database
def add_new_room(old, new, db_send, dir_trav, opp_dir_trav, room_bool):
    if old != new:
        if room_bool:
            requests.post(storage, json=db_send).json()
            print('added room', new)
        requests.put(storage + str(old) + '/', json={dir_trav: new}).json()
        requests.put(storage + str(new) + '/', json={opp_dir_trav: old}).json()
        print('changed room directions', new, '&', old)


def closed_exits(room):
    r_id = str(room['room_id'])
    exits = room['exits']
    dirs = ['n','s','e','w']
    for door in dirs:
        if door not in exits:
            requests.put(storage + r_id + '/', json={door: -100})


# Given a starting room and a list of instructions, this function follows that path
def follow_path(start, path, header_info):
    print('following known path', path)
    rooms_avail = get_room_dict()
    final_room = None
    direction_possibilities = {
        'n': 's',
        's': 'n',
        'e': 'w',
        'w': 'e'
    }
    while len(path) > 0:
        next_dir = path.pop()
        this_move = {"direction": next_dir}
        if start in rooms_avail:
            if rooms_avail[start][next_dir] >= 0:
                this_move["next_room_id"] = str(
                    rooms_avail[start][next_dir])
        print(this_move)
        new_room = requests.post(room_db + 'move/', headers=header_info, json=this_move).json()
        time.sleep(new_room['cooldown'])
        db_send = {
            "id": new_room["room_id"],
            "coordinates": new_room["coordinates"],
            "name": new_room["title"],
            "description": new_room["description"],
        }
        if new_room['room_id'] not in rooms_avail:
            add_new_room(start, new_room['room_id'], db_send,
                         next_dir, direction_possibilities[next_dir], True)
        else:
            add_new_room(start, new_room['room_id'], db_send,
                         next_dir, direction_possibilities[next_dir], False)

        closed_exits(new_room)
        print('traveling back through room', new_room['room_id'])
        start = new_room['room_id']
        final_room = dict(new_room)

    return final_room

# TODO nearest-path and shortest-path are both almost exactly the same
# Finds and returns the shortest path to the nearest unknown room or hallway
def nearest_open_path(start):
    print('finding nearest')
    visited_paths = get_room_dict()
    rooms_visited = set()
    queue = Queue()
    queue.enqueue({"room": start, "path": []})
    found_path = False
    while not found_path:
        curr_path = queue.dequeue()
        curr_room = curr_path["room"]
        path_n = [visited_paths[curr_room]['n'], 'n']
        path_s = [visited_paths[curr_room]['s'], 's']
        path_e = [visited_paths[curr_room]['e'], 'e']
        path_w = [visited_paths[curr_room]['w'], 'w']
        dirs = [path_e, path_n, path_s, path_w]
        for d in dirs:
            if d[0] > -1 and d[0] not in rooms_visited:
                new_path = {"room": d[0], "path": list(curr_path["path"])}
                new_path["path"].insert(0, d[1])
                rooms_visited.add(d[0])
                queue.enqueue(new_path)
            elif d[0] == -1:
                curr_path['path'].insert(0, d[1])
                print("going this way", curr_path['path'])
                return {"room": curr_room, "path": curr_path["path"]}



# Finds and returns the shortest path to a particular room number
def shortest_path_to(dest, start):
    print('finding path to', dest)
    visited_paths = get_room_dict()
    rooms_visited = set()
    queue = Queue()
    queue.enqueue({"room": start, "path": []})
    found_path = False
    while not found_path:
        curr_path = queue.dequeue()
        curr_room = curr_path["room"]
        path_n = [visited_paths[curr_room]['n'], 'n']
        path_s = [visited_paths[curr_room]['s'], 's']
        path_e = [visited_paths[curr_room]['e'], 'e']
        path_w = [visited_paths[curr_room]['w'], 'w']
        dirs = [path_e, path_n, path_s, path_w]
        for d in dirs:
            if d[0] != dest and d[0] > -1 and d[0] not in rooms_visited:
                new_path = {"room": d[0], "path": list(curr_path["path"])}
                new_path["path"].insert(0, d[1])
                rooms_visited.add(d[0])
                queue.enqueue(new_path)
            elif d[0] == dest:
                curr_path['path'].insert(0, d[1])
                print("going this way", curr_path['path'])
                return {"room": curr_room, "path": curr_path["path"]}