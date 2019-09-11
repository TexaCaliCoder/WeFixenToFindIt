import requests
import time
import util
import getters


# These functions serve as info getters
# - retreives the list of known rooms and returns that in dictionary form
def get_room_dict():
    room_dict = {}
    room_list = requests.get(
        util.storage).json()
    for room in room_list:
        room_dict[room['id']] = room

    return room_dict


def get_current_room(header_info):
    room = requests.get(util.room_db + 'init/', headers=header_info).json()
    time.sleep(room['cooldown'])
    return room


# - retreives the current user info
def get_user(header_info):
    user = requests.post(util.room_db + 'status/', headers=header_info).json()
    time.sleep(user['cooldown'])
    return user