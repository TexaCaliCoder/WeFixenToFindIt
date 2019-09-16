import './PlayerStatus.scss'
import React from 'react'

function PlayerStatus(props) {
    const items = props.state.inventory || []
    return (
        <div className="sideBlock">
            <p>Name:{props.state.name}</p>
            <p>Gold:{props.state.gold}</p>
            <p>Encumbrance:{props.state.encumbrance}</p>
            <p>Speed:{props.state.speed}</p>
            <p>Inventory:
              {items.map((item, index) => index === items.length - 1 ? (<span key={index}>{item}</span>) : (<span key={index}>{item}, </span>))}
            </p>
        </div>
    )
}

export default PlayerStatus
