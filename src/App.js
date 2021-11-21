import React, { Component }  from 'react';
import logo from './logo.svg';
import smileySun from './smileySun.png';
import smileySun2 from './smileySun2.png';
import smileySun3 from './smileySun3.png';
import './App.css';

function App() {
  return (
    <div className="App">


      <header className="App-header">
        {"\n"}
        <img src={smileySun3} className="App-logo" alt="smileySun3" />
        <p>
          This will be the Solar Server!
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React, Get to know our team!
        </a>
        <form>
          <label>
            Your Address:
            <input type="text" name="name" />
          </label>
          <input type="submit" value="Submit" />
        </form>
      </header>
    </div>
  );
}

export default App;
