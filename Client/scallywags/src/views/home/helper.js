export default function (rooms) {
  const roomObj = {}
  const coord = [] // [{x: int, y: int}]
  const links = [] // [[coord1, coord2][coord2, coord3]]
  for (let i in rooms) {
    roomObj[rooms[i].id] = rooms[i]
    const location = rooms[i].coordinates
    const x = parseInt(location.slice(1,3))
    const y = parseInt(location.slice(4,6))
    roomObj[rooms[i].id].xy = {x:x, y:y}
    coord.push({x:x, y:y, id:rooms[i].id})
  }
  for (let i in roomObj) {
    const room = roomObj[i]
    if (room.n > 0) {
      links.push([room.xy, roomObj[room.n].xy])
    }
    if (room.e > 0) {
      links.push([room.xy, roomObj[room.e].xy])
    }
    if (room.s > 0) {
      links.push([room.xy, roomObj[room.s].xy])
    }
    if (room.w > 0) {
      links.push([room.xy, roomObj[room.w].xy])
    }
  }
  return [roomObj, coord, links]
}

