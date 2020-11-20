import React from 'react';
import ReactDOM from 'react-dom';
import {Router, Switch, Route} from 'react-router-dom';
import {createBrowserHistory, CreateBrowserHistory} from 'history';
import './index.css';
import App from './components/App';
import Blockchain from './components/Blockchain';
import ConductTransaction from './components/ConductTransaction';

ReactDOM.render(
  <React.StrictMode>
    <Router history={createBrowserHistory()}>
      <Switch>
        <Route path='/' exact component={App} />
        <Route path='/blockchain' component={Blockchain} />
        <Route path='/condut-transaction' component={ConductTransaction} />
      </Switch>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);