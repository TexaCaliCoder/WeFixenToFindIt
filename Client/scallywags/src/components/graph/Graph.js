import React, { Component } from 'react'
import './Graph.scss';
import { FlexibleXYPlot, XAxis, YAxis, HorizontalGridLines, LineSeries, VerticalGridLines, MarkSeries } from 'react-vis';

export default class graph extends Component {
    render() {
        return (
            <div className="graph">
                <h2>Graph Will Go Here</h2>
                <FlexibleXYPlot
                    width={600}
                    height={600}>
                    <HorizontalGridLines />
                    <VerticalGridLines/>
                    <MarkSeries
                    strokeWidth={3}
                    opacity = "1"
                        data={[
                            { x: 1, y: 1 },
                            { x: 2, y: 2 },
                            { x: 3, y:3 },
                            { x: 4, y: 4},
                            { x: -5, y: -5},
                            { x: 2, y: 10}
                        ]} />
                    <XAxis />
                    <YAxis />
                </FlexibleXYPlot>
            </div>
        )
    }
}
