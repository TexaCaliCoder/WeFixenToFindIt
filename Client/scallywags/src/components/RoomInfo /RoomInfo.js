import React from 'react';
import './RoomInfo.scss';

function RoomInfo(props) {
    console.log(props, 'room props')
	return(
        <div className="sideBlock">
            <p>Room Name:{props.state.title} </p>
            <p>Room Coordinates: {props.state.coordinates}</p>
            <p>Items In Room:{props.state.items}</p>
            <p>Players In Room: {props.state.players}:</p>
        </div>
    );
}

export default RoomInfo;
