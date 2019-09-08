import requests
import random
from datetime import datetime, timedelta

traversalPath = []
'''
Depth first traversal to where a path ends at dead end or all explored paths,
then breadth first search to find the closet offshoot that has an unexplored path.
'''
api_key = "Token 508711f53445fa67d8bdc1c97da256eacaef2e5e"
header_info = {'Authorization': api_key}
  # "Token dccec1ad173d2abaf88b542a02095f8d93ea97df",
  # "Token 8271c9035b3a113a16111392722a7bb4d9278a2c",
  # "Token 64936db353e36faa7ec880bb81331706cd4216a7"
timer = {'time': 0, 'purpose': 'move purposefully'}
room_info = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=header_info)
timer['time'] = countdown_setup(room_info['cooldown'])
item_to_get = ''

# this is the regular path
def traversal(player, graph):
  # get room info to use for ```player```
  rooms_to_visit = True
  ## I don't think the following in valid. We are adding the rooms in as part of decision tree
  # for rooms in room_info:
  #   visited_rooms.add(room_info[rooms]['room_id'])
  while rooms_to_visit:

    global room_info
    purpose = timer['purpose']
    user = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/status/', headers=header_info)
    timer['time'] = countdown_setup(user['cooldown'])

    ## for each user, check
    ## - purpose of timer - tells us which actions we are performing
    ## - see if timer time has reached zero

    ## ITEM LOOKUP

    while purpose == "item lookup":
      if len(room_info['items']) == 0:
        purpose = 'move randomly'
      ## check the timer
      if timecheck():
        ## TODO get the info from our database for the room we are in
        for item in room_info['items']:
          item_name = {"name": item['name']}
          pickup = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/', headers=header_info, json=item_name)
          timer['time'] = countdown_setup(pickup['cooldown'])
          if pickup['weight'] + user['encumbrance'] <= user['strength']:
            item_to_get = pickup['name']
            purpose = 'item get'
          else:
            purpose = 'find shop'

    while purpose == "move randomly":
      possible_moves = []
      c_rm = room_info
        ## TODO add in exits info from database version of the room
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
          new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=header_info, json={"direction":move})
          timer['time'] = countdown_setup(new_room['cooldown'])
          ## TODO add post command to add the new room and add the "w" of the new room in our database to the old room id
          ## TODO add put command to change the "e" of the old room in our database
          purpose == "item lookup"

    ## ITEM GET
    while purpose == 'item get':
      if timecheck():
        received_item = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/take/', headers=header_info, json={"name":item_to_get})
        timer['time'] = countdown_setup(received_item['cooldown'])
        purpose = 'item lookup'

    ## DIRECTION DECISION TREE
    ## check timer again
    while purpose == 'move purposefully':
      if timecheck():
        visited_rooms = requests.get("https://wegunnagetit.herokuapp.com/rooms/")
        c_rm = room_info
        ## TODO add in exits info from database version of the room
        c_rm_n = True if 'n' in room_info['exits'] else False
        c_rm_s = True if 's' in room_info['exits'] else False
        c_rm_e = True if 'e' in room_info['exits'] else False
        c_rm_w = True if 'w' in room_info['exits'] else False

        if c_rm_n and c_rm['room_id'] not in visited_rooms:
          visited_rooms.add(c_rm['room_id'])
          old_room = c_rm['room_id']
          new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=header_info, json={"direction":"n"})
          timer['time'] = countdown_setup(new_room["cooldown"])
          db_send = {
            "id": new_room["room_id"],
            "coordinates": new_room["coordinates"],
            "name": new_room["title"],
            "description": new_room["description"],
          }
          ## post new room to db and change directions of new room and old room to reflect new info
          requests.post("https://wegunnagetit.herokuapp.com/rooms/", json=db_send)
          requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(old_room) + '/', json={'n': new_room['room_id']})
          requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'s': old_room})
          room_info = dict(new_room)
        elif c_rm_e and c_rm['room_id'] not in visited_rooms:
          visited_rooms.add(c_rm['room_id'])
          old_room = c_rm['room_id']
          new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=header_info, json={"direction":"e"})
          timer['time'] = countdown_setup(new_room["cooldown"])
          db_send = {
            "id": new_room["room_id"],
            "coordinates": new_room["coordinates"],
            "name": new_room["title"],
            "description": new_room["description"],
          }
          ## post new room to db and change directions of new room and old room to reflect new info
          requests.post("https://wegunnagetit.herokuapp.com/rooms/", json=db_send)
          requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(old_room) + '/', json={'e': new_room['room_id']})
          requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'w': old_room})
          room_info = dict(new_room)
        elif c_rm_s and c_rm['room_id'] not in visited_rooms:
          visited_rooms.add(c_rm['room_id'])
          old_room = c_rm['room_id']
          new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=header_info, json={"direction":"s"})
          timer['time'] = countdown_setup(new_room["cooldown"])
          db_send = {
            "id": new_room["room_id"],
            "coordinates": new_room["coordinates"],
            "name": new_room["title"],
            "description": new_room["description"],
          }
          ## post new room to db and change directions of new room and old room to reflect new info
          requests.post("https://wegunnagetit.herokuapp.com/rooms/", json=db_send)
          requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(old_room) + '/', json={'s': new_room['room_id']})
          requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'n': old_room})
          room_info = dict(new_room)
        elif c_rm_w and c_rm['room_id'] not in visited_rooms:
          visited_rooms.add(c_rm['room_id'])
          old_room = c_rm['room_id']
          new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=header_info, json={"direction":"w"})
          timer['time'] = countdown_setup(new_room["cooldown"])
          db_send = {
            "id": new_room["room_id"],
            "coordinates": new_room["coordinates"],
            "name": new_room["title"],
            "description": new_room["description"],
          }
          ## post new room to db and change directions of new room and old room to reflect new info
          requests.post("https://wegunnagetit.herokuapp.com/rooms/", json=db_send)
          requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(old_room) + '/', json={'w': new_room['room_id']})
          requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new_room['room_id']) + '/', json={'e': old_room})
          room_info = dict(new_room)
        elif len(visited_rooms) <= 500:
          purpose = 'move randomly'
        else:
          last_open = nearest_open_path(c_rm.id, graph, visited_rooms)
          goto_location(last_open["room"], last_open["curr_path"])


def countdown_setup(cooldown):
  return datetime.now() + timedelta(seconds=cooldown)

def timecheck():
  if timer['time'] < datetime.now():
    return True
  else:
    return False

# This is the breadth first search for a room that still has openings
def nearest_open_path(start, graph, visited):
  visited_paths = {}
  queue = Queue()
  queue.enqueue({"room": start, "path": []})
  found_path = False
  while not found_path:
      curr_path = queue.dequeue()
      curr_room = curr_path["room"]
      if curr_room not in visited_paths:
          visited_paths[curr_room] = curr_path
          for d in graph[curr_room][1]:
            if graph[curr_room][1][d] in visited:
              new_path = {"room": graph[curr_room][1][d], "path": list(curr_path["path"])}
              new_path["path"].append(d)
              queue.enqueue(new_path)
            else:
              return {"room": curr_room, "path": curr_path["path"]}

# go to a location
def goto_location(room_id, path):
  while len(path) > 0:
    if timecheck():
      next_dir = path.pop()
      new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=header_info, json={"direction":next_dir})
      timer['time'] = countdown_setup(new_room["cooldown"])


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