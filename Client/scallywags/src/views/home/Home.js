import React, { Component } from 'react';
import './Home.scss';
import Buttons from '../../components/buttons/buttons';
import Graph from '../../components/graph/Graph';
import PlayerStatus from '../../components/PlayerStatus/PlayerStatus';
import RoomInfo from '../../components/RoomInfo /RoomInfo';
import axios from 'axios';

class Home extends Component {
    constructor(props){
        super(props);
        this.state = {
            room_data :[]
        }
    }
    componentDidMount(){
        axios
            .get('https://wegunnagetit.herokuapp.com/rooms/')
            .then(res => this.setState({room_data: res}))
            .catch(err => console.log(err))
    }
	render() {
        console.log(this.state)
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
