import './PlayerStatus.scss'
import React from 'react'

function PlayerStatus(props) {
    console.log(props, 'player status props')
    return (
        <div className="sideBlock">
            <p>Name:</p>
            <p>Gold:</p>
            <p>Encumbrance:</p>
            <p>Speed:</p>
            <p>Inventory:</p>
        </div>
    )
}

export default PlayerStatus
