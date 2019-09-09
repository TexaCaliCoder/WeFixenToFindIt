import requests
import random
from datetime import datetime, timedelta
import time

# traversalPath = []
# '''
# Depth first traversal to where a path ends at dead end or all explored paths,
# then breadth first search to find the closet offshoot that has an unexplored path.
# '''


def countdown_setup(cooldown):
  return datetime.now() + timedelta(seconds=cooldown)

def get_room_dict():
  room_dict = {}
  room_list = requests.get("https://wegunnagetit.herokuapp.com/rooms/").json()
  for room in room_list:
    room_dict[room['id']] = room

  return room_dict

shop = 1
pirate_ry = 467
flying_shrine = 22
ghost_shrine = 499
speed_shrine = 461

api_key = "Token 508711f53445fa67d8bdc1c97da256eacaef2e5e"
header_info = {'Authorization': api_key}
  # "Token dccec1ad173d2abaf88b542a02095f8d93ea97df",
  # "Token 8271c9035b3a113a16111392722a7bb4d9278a2c",
  # "Token 64936db353e36faa7ec880bb81331706cd4216a7",
  # "Token 508711f53445fa67d8bdc1c97da256eacaef2e5e"
timer = {'time': 0, 'purpose': 'move randomly'}
room_info = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=header_info).json()
new_time = countdown_setup(room_info['cooldown'])
timer['time'] = new_time

# item_to_get = ''

rooms_we_have = get_room_dict()

if room_info['room_id'] not in rooms_we_have:
  db_send = {
    "id": room_info["room_id"],
    "coordinates": room_info["coordinates"],
    "name": room_info["title"],
    "description": room_info["description"],
  }
  requests.post("https://wegunnagetit.herokuapp.com/rooms/", json=db_send).json()

def timecheck():
  if timer['time'] < datetime.now():
    return True
  else:
    return False

# this is the regular path
def traversal():
  # get room info to use for ```player```
  rooms_to_visit = True
  items_onboard = []
  global timer
  global room_info
  ## I don't think the following in valid. We are adding the rooms in as part of decision tree
  # for rooms in room_info:
  #   visited_rooms.add(room_info[rooms]['room_id'])
  while rooms_to_visit:

    purpose = "move randomly"

    ## for each user, check
    ## - purpose of timer - tells us which actions we are performing
    ## - see if timer time has reached zero
    def get_user():
      while True:
        if timecheck():
          user = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/status/', headers=header_info).json()
          time.sleep(user['cooldown'])
          return user

    def update_room_info():
      global room_info
      while True:
        if timecheck():
          room_info = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=header_info).json()
          time.sleep(room_info['cooldown'])
          return

    ## ITEM LOOKUP

    def item_lookup():
      global item_to_get
      while True:
        if len(room_info['items']) == 0:
          print('there is nothing left here')
          return

        ## check the timer
        if timecheck():
          user = get_user()

          ## TODO get the info from our database for the room we are in
          item = room_info['items'][0]
          item_name = {"name": item}
          pickup = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/', headers=header_info, json=item_name).json()
          timer['time'] = countdown_setup(pickup['cooldown'])
          print("there is a", pickup['name'])
          if pickup['weight'] + user['encumbrance'] <= user['strength']:
            item_to_get = pickup['name']
            items_onboard.append(item_to_get)
            item_get()
            update_room_info()
          else:
            shop_path = shortest_path_to(shop, room_info['room_id'])
            follow_path(room_info['room_id'], shop_path['path'])
            print('going to sell goods')
            sell_items()
            return

    ## ITEM GET
    def item_get():
      while True:
        if timecheck():
          received_item = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/take/', headers=header_info, json={"name":item_to_get}).json()
          timer['time'] = countdown_setup(received_item['cooldown'])
          print('picked up the', item_to_get)
          return

    def sell_items():
      global timer
      while True:
        confirm = 'no'
        item_to_sell = ""
        if timecheck():
          if len(items_onboard) == 0:
            return
          elif confirm == "no":
            item_to_sell = items_onboard.pop()
            sale = {"name": item_to_sell}
            merchant = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/", headers=header_info, json=sale).json()
            timer = countdown_setup(merchant["cooldown"])
            print('sold the', item_to_sell, merchant["messages"])
            confirm = "yes"
          else:
            sale = {"name": item_to_sell, "confirm": "yes"}
            merchant = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/", headers=header_info, json=sale).json()
            timer = countdown_setup(merchant["cooldown"])
            confirm = 'no'


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

      if timecheck():

        next_room = rooms_we_have[c_rm['room_id']][move]
        db_send = {"direction": move, "next_room_id": str(next_room)} if next_room > -1 else {"direction": move}
        new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=header_info, json=db_send).json()
        print("moved to", new_room['room_id'])
        timer['time'] = countdown_setup(new_room['cooldown'])
        room_info = dict(new_room)
        if next_room == -1:
          add_new_room(c_rm['room_id'], new_room['room_id'], {}, move, direction_possibilities[move], False)
        purpose = "item lookup"
        item_lookup()


    ## DIRECTION DECISION TREE
    ## check timer again
    while purpose == 'move purposefully':
      if timecheck():
        visited_rooms = get_room_dict()

        if room_info['room_id'] not in visited_rooms:
          db_send = {
            "id": room_info["room_id"],
            "coordinates": room_info["coordinates"],
            "name": room_info["title"],
            "description": room_info["description"],
          }
          requests.post("https://wegunnagetit.herokuapp.com/rooms/", json=db_send).json()
          visited_rooms = get_room_dict()

        c_rm = room_info
        c_rm_n = True if 'n' in room_info['exits'] and visited_rooms[c_rm['room_id']]['n'] < 0 and visited_rooms[c_rm['room_id']]['n'] > -100 else False
        c_rm_s = True if 's' in room_info['exits'] and visited_rooms[c_rm['room_id']]['s'] < 0 and visited_rooms[c_rm['room_id']]['s'] > -100 else False
        c_rm_e = True if 'e' in room_info['exits'] and visited_rooms[c_rm['room_id']]['e'] < 0 and visited_rooms[c_rm['room_id']]['e'] > -100 else False
        c_rm_w = True if 'w' in room_info['exits'] and visited_rooms[c_rm['room_id']]['w'] < 0 and visited_rooms[c_rm['room_id']]['w'] > -100 else False

        if c_rm_n:
          old_room = c_rm['room_id']
          new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=header_info, json={"direction":"n"}).json()
          timer['time'] = countdown_setup(new_room["cooldown"])
          db_send = {
            "id": new_room["room_id"],
            "coordinates": new_room["coordinates"],
            "name": new_room["title"],
            "description": new_room["description"],
          }
          ## post new room to db and change directions of new room and old room to reflect new info
          if new_room['room_id'] not in visited_rooms:
            add_new_room(old_room, new_room['room_id'], db_send, "n", "s", True)
          else:
            add_new_room(old_room, new_room['room_id'], db_send, "n", "s", False)
          if "n" not in new_room["exits"]:
            requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'n': -100}).json()
          if "e" not in new_room["exits"]:
            requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'e': -100}).json()
          if "w" not in new_room["exits"]:
            requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'w': -100}).json()
          room_info = dict(new_room)
        elif c_rm_e:
          old_room = c_rm['room_id']
          new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=header_info, json={"direction":"e"}).json()
          timer['time'] = countdown_setup(new_room["cooldown"])
          db_send = {
            "id": new_room["room_id"],
            "coordinates": new_room["coordinates"],
            "name": new_room["title"],
            "description": new_room["description"],
          }
          ## post new room to db and change directions of new room and old room to reflect new info
          if new_room['room_id'] not in visited_rooms:
            add_new_room(old_room, new_room['room_id'], db_send, "e", "w", True)
          else:
            add_new_room(old_room, new_room['room_id'], db_send, "e", "w", False)
          if "n" not in new_room["exits"]:
            requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'n': -100}).json()
          if "e" not in new_room["exits"]:
            requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'e': -100}).json()
          if "s" not in new_room["exits"]:
            requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'s': -100}).json()
          room_info = dict(new_room)
        elif c_rm_s:
          old_room = c_rm['room_id']
          new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=header_info, json={"direction":"s"}).json()
          timer['time'] = countdown_setup(new_room["cooldown"])
          db_send = {
            "id": new_room["room_id"],
            "coordinates": new_room["coordinates"],
            "name": new_room["title"],
            "description": new_room["description"],
          }
          ## post new room to db and change directions of new room and old room to reflect new info
          if new_room['room_id'] not in visited_rooms:
            add_new_room(old_room, new_room['room_id'], db_send, "s", "n", True)
          else:
            add_new_room(old_room, new_room['room_id'], db_send, "s", "n", False)
          if "s" not in new_room["exits"]:
            requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'s': -100}).json()
          if "e" not in new_room["exits"]:
            requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'e': -100}).json()
          if "w" not in new_room["exits"]:
            requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'w': -100}).json()
          room_info = dict(new_room)
        elif c_rm_w:
          old_room = c_rm['room_id']
          new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=header_info, json={"direction":"w"}).json()
          timer['time'] = countdown_setup(new_room["cooldown"])
          db_send = {
            "id": new_room["room_id"],
            "coordinates": new_room["coordinates"],
            "name": new_room["title"],
            "description": new_room["description"],
          }
          ## post new room to db and change directions of new room and old room to reflect new info
          if new_room['room_id'] not in visited_rooms:
            add_new_room(old_room, new_room['room_id'], db_send, "w", "e", True)
          else:
            add_new_room(old_room, new_room['room_id'], db_send, "w", "e", False)


          if "n" not in new_room["exits"]:
            requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'n': -100}).json()
          if "s" not in new_room["exits"]:
            requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'s': -100}).json()
          if "w" not in new_room["exits"]:
            requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'w': -100}).json()
          room_info = dict(new_room)
        elif len(visited_rooms) >= 500:
          print("we're done here")
          rooms_to_visit = False
          purpose = 'move randomly'
        else:
          print('going to find a new way around from room #', c_rm['room_id'])
          last_open = nearest_open_path(c_rm["room_id"])
          room_info = follow_path(c_rm["room_id"], last_open["path"])



# This is the breadth first search for a room that still has openings
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

# go to a location
def follow_path(start, path):
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
    if timecheck():
      next_dir = path.pop()
      this_move = {"direction": next_dir}
      if start in rooms_avail:
        if rooms_avail[start][next_dir] >= 0:
          this_move["next_room_id"] = str(rooms_avail[start][next_dir])
      print(this_move)
      new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=header_info, json=this_move).json()
      timer['time'] = countdown_setup(new_room["cooldown"])
      db_send = {
        "id": new_room["room_id"],
        "coordinates": new_room["coordinates"],
        "name": new_room["title"],
        "description": new_room["description"],
      }
      if new_room['room_id'] not in rooms_avail:
        add_new_room(start, new_room['room_id'], db_send, next_dir, direction_possibilities[next_dir], True)
      else:
        add_new_room(start, new_room['room_id'], db_send, next_dir, direction_possibilities[next_dir], False)

      if "n" not in new_room["exits"]:
        requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'n': -100}).json()
      if "s" not in new_room["exits"]:
        requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'s': -100}).json()
      if "w" not in new_room["exits"]:
        requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'w': -100}).json()
      if "e" not in new_room["exits"]:
        requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'e': -100}).json()
      print('traveling back through room', new_room['room_id'])
      start = new_room['room_id']
      final_room = dict(new_room)

  return final_room


def add_new_room(old, new, db_send, dir_trav, opp_dir_trav, room_bool):
    if old != new:
      if room_bool:
        requests.post("https://wegunnagetit.herokuapp.com/rooms/", json=db_send).json()
        print('added room', new)
      requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(old) + '/', json={dir_trav: new}).json()
      requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new) + '/', json={opp_dir_trav: old}).json()
      print('changed room directions', new, '&', old)

def go_shopping(start):
    shop_path = shortest_path_to(shop, start)
    follow_path(start, shop_path['path'])
    ## TODO go_shopping
    # get user info
    # while there are items
      # if the timer is up
        # pop an item off
        # sell an item
    # go back to starting room and randomly move

## TODO go to a shrine
## TODO set check for 1000 gold and travel to Pirate Ry

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


traversalPath = []
'''
Depth first traversal to where a path ends at dead end or all explored paths,
then breadth first search to find the closet offshoot that has an unexplored path.
'''


traversal()