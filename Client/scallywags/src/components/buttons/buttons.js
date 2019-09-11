import React, { Component } from 'react';
import './buttons.scss';
import { button } from 'react-router-dom';

class Buttons extends Component {
	render() {
		return (
			<div className="buttonBar">
				<button className="directionButton">North</button>
                <button className="directionButton">South</button>
                <button className="directionButton">East</button>
                <button className="directionButton">West</button>
			</div>
		);
	}
}

export default Buttons;
