import React, { Component } from 'react';
import './Home.scss';
import Buttons from '../../components/buttons/buttons';
import Graph from '../../components/graph/Graph';
import PlayerStatus from '../../components/PlayerStatus/PlayerStatus';
import RoomInfo from '../../components/RoomInfo /RoomInfo';
import axios from 'axios';
import helper from './helper';

class Home extends Component {
	constructor(props) {
		super(props);
		this.state = {
			room_data: [],
			coordinates: [],
			links: []
		};
	}
	componentDidMount() {
		axios
			.get('https://wegunnagetit.herokuapp.com/rooms/')
			.then((res) => {
				const rooms = helper(res.data);
				this.setState({ room_data: rooms[0], coordinates: rooms[1], links: rooms[2] });
			})
			.catch((err) => console.log(err));
	}
	render() {
		console.log(this.state);
		return (
			<div>
				<h1>Lambda Treasure Hunt</h1>
				<div className='graphContainer'>
					<Graph className='graph' state={this.state} />
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
