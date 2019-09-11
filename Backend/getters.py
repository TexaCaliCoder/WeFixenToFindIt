import requests
import time
import util
 


# These functions serve as info getters
# - retreives the list of known rooms and returns that in dictionary form
def get_room_dict():
    room_dict = {}
    room_list = requests.get(
        util.storage).json()
    for room in room_list:
        room_dict[room['id']] = room

    return room_dict


def get_current_room():
    room = requests.get(util.room_db + 'init/', headers=util.header_info).json()
    time.sleep(room['cooldown'])
    return room


# - retreives the current user info
def get_user():
    user = requests.post(util.room_db + 'status/', headers=util.header_info).json()
    time.sleep(user['cooldown'])
    return user


def item_lookup(items_onboard):
    while True:
        room_info = get_current_room()
        if len(room_info['items']) == 0:
            print('there is nothing left here')
            return items_onboard

        user = get_user()

        item = room_info['items'][0]
        item_name = {"name": item}
        pickup = requests.post(
            util.room_db + 'examine/', headers=util.header_info, json=item_name).json()
        time.sleep(pickup['cooldown'])
        print("there is a", pickup['name'])
        if pickup['weight'] + user['encumbrance'] <= user['strength']:
            items_onboard.append(pickup['name'])
            item_get(pickup['name'])
        else:
            shop_path = util.shortest_path_to(util.shop, room_info['room_id'])
            util.follow_path(room_info['room_id'],
                        shop_path['path'], util.header_info)
            print('going to sell goods')
            util.sell_items(items_onboard)
            return []


def item_get(item_to_get):
    received_item = requests.post(util.room_db + 'take/', headers=util.header_info, json={"name": item_to_get}).json()
    time.sleep(received_item['cooldown'])
    print('picked up the', item_to_get)
    return