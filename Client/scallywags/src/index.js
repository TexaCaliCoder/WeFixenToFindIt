import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { BrowserRouter as Router } from 'react-router-dom'
import 'bootstrap/dist/css/bootstrap.min.css';
require('dotenv').config()


ReactDOM.render(<Router><App /></Router>, document.getElementById('root'));


