import React, { Component } from 'react';
import './Graph.scss';
import {
  FlexibleXYPlot,
  XAxis,
  YAxis,
  HorizontalGridLines,
  LineSeries,
  VerticalGridLines,
  MarkSeries
} from 'react-vis';

class graph extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    const { coordinates, links, current_room_info } = this.props.state;
    const currentRoom = current_room_info.room_id;
    const shop = 1;
    const pirate_ry = 467;
    const shrine = [22, 499, 461];
    const mine = 250;
    const color = 'fff000';
    return (
      <div className="graph">
        <FlexibleXYPlot width={800} height={600}>
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
              size={
                item.id === currentRoom
                  ? 10
                  : item.id === shop
                  ? 6
                  : item.id === mine
                  ? 6
                  : shrine.includes(item.id)
                  ? 6
                  : 3
              }
              color={
                item.id === currentRoom
                  ? 'ff0000'
                  : item.id === shop
                  ? '23ff00'
                  : item.id === mine
                  ? '00fbff'
                  : shrine.includes(item.id)
                  ? '1b00ff'
                  : 'ffff00'
              }
              onSeriesClick = {() => console.log(item.id)}
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
