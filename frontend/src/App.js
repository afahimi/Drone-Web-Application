// import './App.css';
import { Fragment } from 'react';
import './bootstrap/bootstrap.css';
import Toggle from './components/toggle-button';
// import Switch from "./Switch"; //unused import
import CheckSwitch from './components/CheckSwitch';
import Canvas from './components/Canvas'

import './index.css';

function App() {
  return (
    <Fragment>
        <div className="App">
        <Canvas />
        <Toggle />
      </div>
    </Fragment>
  );
}


export default App;
