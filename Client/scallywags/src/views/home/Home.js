import React, { Component } from 'react';
import { Dropdown, DropdownButton } from 'react-bootstrap';
import './Home.scss';
import Graph from '../../components/graph/Graph';
import PlayerStatus from '../../components/PlayerStatus/PlayerStatus';
import RoomInfo from '../../components/RoomInfo/RoomInfo';
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
      api_key: '508711f53445fa67d8bdc1c97da256eacaef2e5e',
      login: true,
      cooldown: 1000
    };
  }
  componentDidMount() {
    this.updateState();
  }

  playerStatus = () => {
    const data = {};
    const options = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${this.state.api_key} `
      }
    };
    axios
      .post(
        'https://lambda-treasure-hunt.herokuapp.com/api/adv/status',
        data,
        options
      )
      .then(response =>
        this.setState({
          player_info: response.data,
          cooldown: response.data.cooldown * 1000 + 5
        })
      )
      .catch(err => console.log(err));
  };

  currRoom = () => {
    const options = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${this.state.api_key}`
      }
    };
    axios
      .get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init', options)
      .then(response => {
        this.setState({
          current_room_info: response.data,
          cooldown: response.data.cooldown * 1000 + 5
        });
        setTimeout(() => {
          this.playerStatus();
        }, this.state.cooldown);
      })
      .catch(err => console.log(err));
  };

  moveRooms = e => {
    const secondary = this.state.room_data[
      this.state.current_room_info.room_id
    ][e.target.name].toString();
    const options = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${this.state.api_key}`
      }
    };
    const body = JSON.stringify({
      direction: e.target.name,
      next_room_id: secondary
    });
    console.log(options, body, 'Here');
    axios
      .post(
        'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', body,
        options
      )
      .then(response => {
        this.setState({
          current_room_info: response.data,
          cooldown: response.data.cooldown * 1000 + 500
        });
        console.log('response', response.data);
      })
      .catch(err => console.log(err));
  };

  updateState = () => {
    const data = {};
    const options = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${this.state.api_key}`
      }
    };
    axios
      .get('https://wegunnagetit.herokuapp.com/rooms/')
      .then(res => {
        const rooms = helper(res.data);
        this.setState({
          room_data: rooms[0],
          coordinates: rooms[1],
          links: rooms[2]
        });
      })
      .catch(err => console.log(err));

    setTimeout(() => {
      this.currRoom();
    }, this.state.cooldown);
  };

  login = e => {
    console.log('click', e.target);
    const name = e.target.name;
    this.setState({ api_key: name, login: true });
    this.updateState();
  };

  render() {
    console.log(this.state);

    return !this.state.login ? (
      // <div>
      // 	<Dropdown options={options} onChange={(option) => {this.setState({api_key: option.label, login: true})}} />
      // </div>
      <DropdownButton id="dropdown-basic-button" title="SELECT YOUR TRAVELER">
        <Dropdown.Item
          onClick={() => this.login()}
          name="64936db353e36faa7ec880bb81331706cd4216a7"
        >
          CHRIS
        </Dropdown.Item>
        <Dropdown.Item
          onClick={this.login}
          name="508711f53445fa67d8bdc1c97da256eacaef2e5e"
        >
          LITTLETON
        </Dropdown.Item>
        <Dropdown.Item
          onClick={this.login}
          name="dccec1ad173d2abaf88b542a02095f8d93ea97df"
        >
          TREW
        </Dropdown.Item>
        <Dropdown.Item
          onClick={this.login}
          name="8271c9035b3a113a16111392722a7bb4d9278a2c"
        >
          DEWAYNE
        </Dropdown.Item>
      </DropdownButton>
    ) : (
      <div>
        <h1>Lambda Treasure Hunt</h1>
        <div className="graphContainer">
          <Graph className="graph" state={this.state} />
          <div className="sideBar">
            <RoomInfo state={this.state.current_room_info} />
            <PlayerStatus state={this.state.player_info} />
          </div>
        </div>
        <div className="buttonBar">
          <button className="directionButton" name="n" onClick={this.moveRooms}>
            North
          </button>
          <button className="directionButton" name="s" onClick={this.moveRooms}>
            South
          </button>
          <button className="directionButton" name="e" onClick={this.moveRooms}>
            East
          </button>
          <button className="directionButton" name="w" onClick={this.moveRooms}>
            West
          </button>
          <button
            className="directionButton"
            onClick={() => this.setState({ login: false })}
          >
            Logout
          </button>
        </div>
      </div>
    );
  }
}

export default Home;
