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
			links: [],
			current_room_info: {},
			player_info: {},
		};
	}
	componentDidMount() {
		const data = {};
		const options = {
			headers: {
				'Content-Type': 'application/json',
				Authorization: 'Token dccec1ad173d2abaf88b542a02095f8d93ea97df',
			},
		};
		axios
			.get('https://wegunnagetit.herokuapp.com/rooms/')
			.then((res) => {
				const rooms = helper(res.data);
				this.setState({ room_data: rooms[0], coordinates: rooms[1], links: rooms[2] });
			})
			.catch((err) => console.log(err));

		setInterval(() => {
			axios
				.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init', options)
				.then((response) => this.setState({ current_room_info: response.data }))
				.catch((err) => console.log(err));
		}, 7000);

		setInterval(() => {
			axios
				.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/status', data, options)
				.then((response) => console.log(response))
				.catch((err) => console.log(err));
		}, 9000);
	}
	render() {
		console.log(this.state);
		return (
			<div>
				<h1>Lambda Treasure Hunt</h1>
				<div className='graphContainer'>
					<Graph className='graph' state={this.state} />
					<div className='sideBar'>
						<RoomInfo state={this.state.current_room_info} />
						<PlayerStatus state={this.state.player_info} />
					</div>
				</div>
				<Buttons />
			</div>
		);
	}
}

export default Home;
