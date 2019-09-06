import React, { Component } from 'react';
import './Home.scss';
import Buttons from '../../components/buttons/Buttons';
import Graph from '../../components/graph/Graph';
import PlayerStatus from '../../components/PlayerStatus/PlayerStatus';
import RoomInfo from '../../components/RoomInfo /RoomInfo';

class Home extends Component {
	render() {
		return (
			<div>
				<h1>Lambda Treasure Hunt</h1>
				<div className='graphContainer'>
					<Graph className='graph' />
					<div className='sideBar'>
						<RoomInfo />
						<PlayerStatus />
					</div>
				</div>
				<Buttons />
			</div>
		);
	}
}

export default Home;
