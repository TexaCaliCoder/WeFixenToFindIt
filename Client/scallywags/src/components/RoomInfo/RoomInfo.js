import React from 'react';
import './RoomInfo.scss';

function RoomInfo(props) {
  const players = props.state.players || []
  const items = props.state.items || []
	return(
        <div className="sideBlock">
            <p>Room Name: {props.state.title} </p>
            <p>Room Coordinates: {props.state.coordinates}</p>
            <p>Items In Room: {items.map((item, index) => index === items.length - 1 ? (<span key={index}>{item}</span>) : (<span key={index}>{item}, </span>))}</p>
            <p>Players In Room:
              {players.map((player, index) => index === players.length - 1 ? (<span key={index}>{player}</span>) : (<span key={index}>{player}, </span>))}
            </p>
        </div>
    );
}

export default RoomInfo;
