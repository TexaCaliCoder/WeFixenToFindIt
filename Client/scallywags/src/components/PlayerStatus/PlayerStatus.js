import './PlayerStatus.scss'
import React from 'react'

function PlayerStatus(props) {
  
    return (
        <div className="sideBlock">
            <p>Name:{props.state.name}</p>
            <p>Gold:{props.state.gold}</p>
            <p>Encumbrance:{props.state.encumbrance}</p>
            <p>Speed:{props.state.speed}</p>
            <p>Inventory:{props.state.inventory}</p>
        </div>
    )
}

export default PlayerStatus
