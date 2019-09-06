import requests
import random

# send init command

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
timer = {'time': 0, 'purpose': 'item lookup'}
room_info = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=header_info)
item_to_get = ''

# this is the regular path
def traversal(player, graph):
  # get room info to use for ```player```
  rooms_to_visit = True
  visited_rooms = set()
  ## I don't think the following in valid. We are adding the rooms in as part of decision tree
  # for rooms in room_info:
  #   visited_rooms.add(room_info[rooms]['room_id'])
  while rooms_to_visit:

    purpose = timer['purpose']
    time = timer['time']
    user = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/status/', headers=header_info)
    ## TODO post user status into our version of user
    ## TODO post room data into our version of the room 
    time = user['cooldown']

    ## for each user, check
    ## - purpose of timer - tells us which actions we are performing
    ## - see if timer time has reached zero

    ## ITEM LOOKUP
    while purpose == "item lookup":
      if len(room_info['items']) == 0:
        purpose = 'move'
      ## check the timer
      if time <= 0:
      ## TODO get the info from our database for the room we are in
        for item in room_info['items']:
          item_name = {"name": item['name']}
          pickup = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/', headers=header_info, json=item_name)
          time = pickup['cooldown']
          if pickup['weight'] + user['encumbrance'] <= user['strength']:
            item_to_get = pickup['name']
            purpose = 'item get'
          else:
            purpose = 'find shop'
          
    ## ITEM GET
    while purpose == 'item get':
      if time <= 0:
        received_item = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/take/', headers=header_info, json={"name":item_to_get})
        time = received_item['cooldown']
        purpose = 'item lookup'

    ## DIRECTION DECISION TREE
    ## check timer again
    c_rm = room_info[room]
    c_rm_n = True if 'n' in room_info[room]['exits'] and blahblahblah['n'] is not Null else False
    c_rm_s = True if 's' in room_info[room]['exits'] else False
    c_rm_e = True if 'e' in room_info[room]['exits'] else False
    c_rm_w = True if 'w' in room_info[room]['exits'] else False

    if c_rm_n and c_rm['room_id'] not in visited_rooms:
      visited_rooms.add(c_rm['room_id'])
      new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers={'Authorization': api_keys[room]}, json={"direction":"n"})
      timers[room] = new_room["cooldown"]
      ## add post command to add the new room and add the "s" of the new room in our database to the old room id
      ## add put command to change the "n" of the old room in our database
      room_info[room] = dict(new_room)
    elif c_rm_e and c_rm['room_id'] not in visited_rooms:
      visited_rooms.add(c_rm['room_id'])
      requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers={'Authorization': api_keys[room]}, json={"direction":"e"})
    elif c_rm_s and c_rm['room_id'] not in visited_rooms:
      visited_rooms.add(c_rm['room_id'])
      requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers={'Authorization': api_keys[room]}, json={"direction":"s"})
    elif c_rm_w and c_rm['room_id'] not in visited_rooms:
      visited_rooms.add(c_rm['room_id'])
      requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers={'Authorization': api_keys[room]}, json={"direction":"w"})
    elif len(roomGraph.keys()) == len(visited_rooms):
      rooms_to_visit = False
    else:
      last_open = nearest_open_path(c_rm.id, graph, visited_rooms)
      for d in last_open['path']:
        traversalPath.append(d)
        player.travel(d)



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

# go to shop and sell items

traversal(player, roomGraph)

# TRAVERSAL TEST
visited_rooms = set()
player.currentRoom = world.startingRoom
visited_rooms.add(player.currentRoom)
for move in traversalPath:
    player.travel(move)
    visited_rooms.add(player.currentRoom)

if len(visited_rooms) == len(roomGraph):
    print(f"TESTS PASSED: {len(traversalPath)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(roomGraph) - len(visited_rooms)} unvisited rooms")


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
#######
# UNCOMMENT TO WALK AROUND
#######
# player.currentRoom.printRoomDescription(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     else:
#         print("I did not understand that command.")
