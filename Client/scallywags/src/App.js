import React from 'react';
import './App.scss';
import Home from './views/home/Home';
import { Route } from 'react-router-dom';

function App() {
	return (
		<div className='App'>
			<Route path='/' component={Home} />
		</div>
	);
}

export default App;
