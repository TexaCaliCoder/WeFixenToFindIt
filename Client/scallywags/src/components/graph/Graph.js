import React, { Component } from 'react';
import './Graph.scss';
import {
  FlexibleXYPlot,
  XAxis,
  YAxis,
  LineSeries,
  MarkSeries
} from 'react-vis';

class graph extends Component {

  render() {
    const { coordinates, links, current_room_info } = this.props.state;
    const currentRoom = current_room_info.room_id;
    const shop = 1;
    const pirate_ry = 467;
    const shrine = [22, 499, 461];
    const mine = 250;
    const transmog = 495
    return (
      <div className="graph">
        <FlexibleXYPlot width={950} height={700}>
          {links.map(item => (
            <LineSeries
              strokeWidth="2"
              color="#FFFFFF"
              data={item}
              key={Math.random() * 100}
            />
          ))}
          {coordinates.map(item => (
            <MarkSeries
              data={[item]}
              name={item.id}
              key={item.id}
              size={
                item.id === currentRoom
                  ? 10
                  : item.id === shop || item.id === mine || item.id === pirate_ry || item.id === transmog || shrine.includes(item.id)
                  ? 6
                  : 4
              }
              color={
                item.id === currentRoom
                  ? 'ff0000'
                  : item.id === shop
                  ? '23ff00'
                  : item.id === mine
                  ? '00fbff'
                  : item.id === pirate_ry
                  ? '02222f'
                  : item.id === transmog
                  ? 'f500ff'
                  : shrine.includes(item.id)
                  ? '1b00ff'
                  : 'ffff00'
              }
              onValueClick = {(val, e) => this.props.travel(val)}
              style={{ cursor: 'pointer' }}
            />
          ))}
          <XAxis />
          <YAxis />
        </FlexibleXYPlot>
      </div>
    );
  }
}

export default graph;
