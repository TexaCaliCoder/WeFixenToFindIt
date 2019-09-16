

export default function (start, dest, room_obj) {
  const rooms_visited = new Set()
  const queue = [{room: start*1, path: []}]
  while (true) {
    const curr_path = queue.shift()
    const curr_room = curr_path.room
    if (curr_room === dest) {
      console.log(curr_path.path)
      return curr_path.path
    }
    let path_n = [room_obj[curr_room].n, 'n']
    let path_s = [room_obj[curr_room].s, 's']
    let path_w = [room_obj[curr_room].w, 'w']
    let path_e = [room_obj[curr_room].e, 'e']
    let dirs = [path_e, path_n, path_s, path_w]
    for (let i in dirs) {
      const d = dirs[i]
      // console.log(d[0] > -1, !(rooms_visited.has(d[0])))
      if (d[0] > -1 && !(rooms_visited.has(d[0]))) {
        const new_path = {room:d[0], path: [...curr_path.path]}
        new_path.path.push(d[1])
        rooms_visited.add(d[0])
        queue.push(new_path)
      }
    }
  }
}


