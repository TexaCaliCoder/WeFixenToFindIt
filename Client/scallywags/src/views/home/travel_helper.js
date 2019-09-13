

export default function (start, dest, room_obj) {
  const rooms_visited = new Set()
  const queue = [{room: start*1, path: []}]
  let found_path = false
  while (!found_path) {
    const curr_path = queue.pop()
    const curr_room = curr_path.room
    if (curr_room === dest) {
      return curr_path.path
    }
    let path_n = [room_obj[curr_room].n, 'n']
    let path_s = [room_obj[curr_room].s, 's']
    let path_w = [room_obj[curr_room].w, 'w']
    let path_e = [room_obj[curr_room].e, 'e']
    let dirs = [path_e, path_n, path_s, path_w]
    for (let i in dirs) {
      const d = dirs[i]
      if (d[0] != dest && d[0] > -1 && !(d[0] in rooms_visited)) {
        const new_path = {room:d[0], path: [...curr_path.path]}
        new_path.path.unshift(d[1])
        rooms_visited.add(d[0])
        queue.push(new_path)
      }
    }
  }
}

// def shortest_path_to(dest, start):
//     print('finding path to', dest)
//     visited_paths = get_room_dict()
//     rooms_visited = set()
//     queue = Queue()
//     queue.enqueue({"room": start, "path": []})
//     found_path = False
//     while not found_path:
//         curr_path = queue.dequeue()
//         curr_room = curr_path["room"]
//         if curr_room == dest:
//             return curr_path
//         path_n = [visited_paths[curr_room]['n'], 'n']
//         path_s = [visited_paths[curr_room]['s'], 's']
//         path_e = [visited_paths[curr_room]['e'], 'e']
//         path_w = [visited_paths[curr_room]['w'], 'w']
//         dirs = [path_e, path_n, path_s, path_w]
//         for d in dirs:
//             if d[0] != dest and d[0] > -1 and d[0] not in rooms_visited:
//                 new_path = {"room": d[0], "path": list(curr_path["path"])}
//                 new_path["path"].insert(0, d[1])
//                 rooms_visited.add(d[0])
//                 queue.enqueue(new_path)
//             elif d[0] == dest:
//                 curr_path['path'].insert(0, d[1])
//                 print("going this way", curr_path['path'])
//                 return {"room": curr_room, "path": curr_path["path"]}

