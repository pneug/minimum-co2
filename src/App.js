import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

var address_input = "test";

// window.open("http://127.0.0.1:5000/address/'goethestr 9, 40670 Meerbusch'");

//$(function () {
//  $('#address-field').on('submit', function (e) {

    //$.ajax({
    //  type: 'post',
    //  url: 'myPageName.php',
    //  data: $('#address-field').serialize(),
    //  success: function () {
    //    alert("Email has been sent!");
    //  }
    //});
//    this.App.state.userInput = $('#address-input').val();
//    e.preventDefault();
//  });
//});

//function onSubmit () {
//  console.log("submit");
//  this.App.state.userInput = "Updated";
//  return false;
//}

//("#address-field").click( function() {
//  var url = "http://127.0.0.1:5000/address/" + $("#address-field").val();
//  window.open(url);
//});

//function App() {
class App extends Component {
  state = {
    userInput: ''
  }

  inputSubmittedHandler = async (event) => {
    event.preventDefault();
    this.setState({ userInput: "loading..." });
    // get the data from the website "http://127.0.0.1:5000/address/'goethestr 9, 40670 Meerbusch'"
    var url = "http://127.0.0.1:5000/address/'" + event.target.value + "'"
    const myInit = {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      },
      mode: 'cors',
      cache: 'default'
    };
    fetch(url, myInit).then(response => {
      response.json().then(response => {
        console.log(response);
        this.setState({ userInput: ("Area: " + response["area"]) });

        const init_segmented_img = {
          method: 'GET',
          headers: {
            'Accept': 'image/png'
          },
          mode: 'cors',
          cache: 'default'
        };
        fetch("http://127.0.0.1:5000/get-by-id/" + response["id"], init_segmented_img).then(response => {
          response.blob().then(response => {
            console.log(response);
            var url = URL.createObjectURL(response);
            var img = new Image();
            img.src = url;
            document.body.appendChild(img);
          });
        }).catch(error => {
          this.setState({ userInput: "Error getting seg img: " + error });
        });

      }).catch(error => {
        this.setState({ userInput: "Json error: " + error });
      })

    }).catch(response => {
      this.setState({ response });
    })
    
    // window.open("http://127.0.0.1:5000/address/'goethestr 9, 40670 Meerbusch'");
    return false;
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            This will be the Solar Server! qw
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
          <form>
            <label>
              Your Address:
              <input type="text" id="address-field" name="address-field" />
            </label>
            <input type="button" value="Submit" onClick={this.inputSubmittedHandler} />
          </form>

          <p>{this.state.userInput}</p>
        </header>
      </div>
    );
  }
}

export default App;
