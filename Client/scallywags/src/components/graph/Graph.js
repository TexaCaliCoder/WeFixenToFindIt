import React, { Component } from 'react'
import './Graph.scss';
import { FlexibleXYPlot, XAxis, YAxis, HorizontalGridLines, LineSeries, VerticalGridLines, MarkSeries } from 'react-vis';

const currentRoom = 34
 class graph extends Component {
     constructor(props){
         super(props)
     }
    render() {
        const {coordinates, links} = this.props.state
        console.log(this.props.state, 'state from props')
        return (
            <div className="graph">
                <FlexibleXYPlot
                    width={800}
                    height={600}>
                    {links.map(item => (<LineSeries 
                        strokeWidth='2' 
                        color="#FFFFFF"
                        data={item}
                        key={Math.random() * 100}
                    />))}
                    {coordinates.map(item => (<MarkSeries
                        data={[item]} 
                        color = {item.id === currentRoom ? "#00ffff" : "ffff00" }
                        style={{ cursor: "pointer" }}
                    />))}
                    <XAxis />
                    <YAxis />
                </FlexibleXYPlot>
            </div>
        )
    }
}

export default graph