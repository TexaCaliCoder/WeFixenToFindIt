import requests

## Basic Queue function
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


## This function adds room information into the datab
def add_new_room(old, new, db_send, dir_trav, opp_dir_trav, room_bool):
    if old != new:
      if room_bool:
        requests.post("https://wegunnagetit.herokuapp.com/rooms/", json=db_send).json()
        print('added room', new)
      requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(old) + '/', json={dir_trav: new}).json()
      requests.put("https://wegunnagetit.herokuapp.com/rooms/" + str(new) + '/', json={opp_dir_trav: old}).json()
      print('changed room directions', new, '&', old)