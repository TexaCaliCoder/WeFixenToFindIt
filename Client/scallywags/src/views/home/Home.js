import React, { Component } from 'react';
import { Dropdown, DropdownButton, Button } from 'react-bootstrap';
import './Home.scss';
import Graph from '../../components/graph/Graph';
import PlayerStatus from '../../components/PlayerStatus/PlayerStatus';
import RoomInfo from '../../components/RoomInfo/RoomInfo';
import axios from 'axios';
import helper from './helper';
import travel from './travel_helper';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      room_data: {},
      coordinates: [],
      links: [],
      current_room_info: {},
      player_info: {},
      api_key: '508711f53445fa67d8bdc1c97da256eacaef2e5e',
      login: true,
      cooldown: 0,
      grey: false,
      spec_cd:0
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
          cooldown: response.data.cooldown * 1000 + 5,
          grey: false
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
          cooldown: response.data.cooldown * 1000 + 5,
          grey: false
        });
        setTimeout(() => {
          this.playerStatus();
          this.setState({cooldown: 0})
        }, this.state.cooldown);
      })
      .catch(err => console.log(err));
  };

  TravelTo = async (dirArr) =>{
    for (let i in dirArr) {
      const d = dirArr[i]
      await this.sleepMove(d)

    }
    alert('done')
  }

  justPause = () => {
    return new Promise(resolve => setTimeout(resolve, 200))
  }

  sleepMove = async (dir) => {
    await this.moveRooms({target:{name:dir}})
    await this.justPause()
    return new Promise(resolve => setTimeout(resolve, this.state.spec_cd)).then(item => item)
  }

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
    console.log(body)
    axios
      .post(
        'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', body,
        options
      )
      .then(response => {
        this.setState({
          current_room_info: response.data,
          cooldown: response.data.cooldown * 1000 + 5,
          grey: false,
          spec_cd: response.data.cooldown * 1000 + 5
        });
      })
      .catch(err => console.log(err));
  };

  updateState = () => {
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
      this.setState({cooldown: 0})
    }, this.state.cooldown);
  };

  login = e => {
    const name = e.target.name;
    this.setState({ api_key: name, login: true });
    this.updateState();
  };

  greyButtons = () => {
    setTimeout(() => {
      this.setState({cooldown: 0, grey: true})
    }, this.state.cooldown)
  }

  travelPath = (val) => {
    const path = travel(this.state.current_room_info.room_id, val.id, this.state.room_data)
    this.TravelTo(path)
  }

  render() {

    if (this.state.cooldown > 0) {
      this.greyButtons()
    }
    let this_room = {}
    if (Object.entries(this.state.room_data).length > 1) {
      const curr_id = this.state.current_room_info.room_id
      this_room = this.state.room_data[curr_id]
    }

    return !this.state.login ? (
      // <div>
      // 	<Dropdown options={options} onChange={(option) => {this.setState({api_key: option.label, login: true})}} />
      // </div>
      <DropdownButton id="dropdown-basic-button" title="SELECT YOUR TRAVELER">
        <Dropdown.Item
          onClick={this.login}
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
      <div className="homeWrapper">
        <h1>Lambda Treasure Hunt</h1>
        <div className="graphContainer">
          <Graph className="graph" state={this.state} travel={this.travelPath} />
          <div className="sideBar">
            <RoomInfo state={this.state.current_room_info} />
            <PlayerStatus state={this.state.player_info} />
          </div>
        </div>
        <div className="buttonBar">
          <Button className="directionButton" disabled={!this.state.grey || this_room.n < 0} name="n" onClick={this.moveRooms}>
            North
          </Button>
          <Button className="directionButton" disabled={!this.state.grey || this_room.s < 0} name="s" onClick={this.moveRooms}>
            South
          </Button>
          <Button className="directionButton" disabled={!this.state.grey || this_room.e < 0} name="e" onClick={this.moveRooms}>
            East
          </Button>
          <Button className="directionButton" disabled={!this.state.grey || this_room.w < 0} name="w" onClick={this.moveRooms}>
            West
          </Button>
          <Button
            className="directionButton" disabled={!this.state.grey}
            onClick={() => this.setState({ login: false })}
          >
            Logout
          </Button>
        </div>
      </div>
    );
  }
}

export default Home;
