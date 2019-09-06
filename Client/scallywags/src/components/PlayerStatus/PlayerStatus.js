import React, { Component } from 'react'
import './PlayerStatus.scss'

export default class PlayerStatus extends Component {
    render() {
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
}
