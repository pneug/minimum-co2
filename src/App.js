import React, { Component } from 'react';
import logo from './logo.svg';
import smileySun from './smileySun.png';
import smileySun2 from './smileySun2.png';
import smileySun3 from './smileySun3.png';
import './App.css';
import placeholder_segmentation from './transparent.png';

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
//    this.App.state.area = $('#address-input').val();
//    e.preventDefault();
//  });
//});

//function onSubmit () {
//  console.log("submit");
//  this.App.state.area = "Updated";
//  return false;
//}

//("#address-field").click( function() {
//  var url = "http://127.0.0.1:5000/address/" + $("#address-field").val();
//  window.open(url);
//});

//function App() {
class App extends Component {
  state = {
    area: '',
    kwh_per_year: '',
    mwh_per_life: '',
    co2_per_year: '',
    co2_per_life: '',
    price_per_kwh: '0.31',
    id: 0
  }

  inputSubmittedHandler = async (event) => {
    event.preventDefault();
    this.setState({ area: "loading..." });
    // get the data from the website "http://127.0.0.1:5000/address/'goethestr 9, 40670 Meerbusch'/0.27"
    var address = document.getElementById("address-field").value;
    var price_per_kwh = document.getElementById("kwh-price").value;
    var url = "http://127.0.0.1:5000/address/'" + address + "'/" + price_per_kwh;
    this.setState({ kwh_per_year: ("URL: " + url) });
    const myInit = {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      },
      mode: 'cors',
      cache: 'no-store'
    };
    fetch(url, myInit).then(response => {
      response.json().then(response => {
        console.log(response);
        this.setState({ area: ("Area: " + response["area"] + "m^2") });
        this.setState({ kwh_per_year: ("kWh per year: " + response["kwh_per_year"] + "kWh") });
        this.setState({ mwh_per_life: ("mWh per life: " + response["mwh_per_life"] + "mWh") });
        this.setState({ co2_per_year: ("CO2 per year: " + response["co2_per_year"] + "kg CO2") });
        this.setState({ co2_per_life: ("CO2 per life: " + response["co2_per_life"] + "kg CO2") });
        this.setState({ id: response["id"] });

        const init_segmented_img = {
          method: 'GET',
          headers: {
            'Accept': 'image/png'
          },
          mode: 'cors',
          cache: 'no-store'
        };
        fetch("http://127.0.0.1:5000/get-by-id/" + response["id"], init_segmented_img).then(response => {
          response.blob().then(response => {
            console.log(response);
            var url = URL.createObjectURL(response);
            var img = new Image();
            img.src = url;
            document.getElementById("seg-img").src = url;
            // document.body.appendChild(img);

            fetch("http://127.0.0.1:5000/get-graph/" + this.state.id, init_segmented_img).then(response => {
              response.blob().then(response => {
                console.log(response);
                var url2 = URL.createObjectURL(response);
                var img2 = new Image();
                img2.src = url;
                document.getElementById("graph-img").src = url2;
                // document.body.appendChild(img2);
              });
            }).catch(error => {
              this.setState({ area: "Error getting graph img: " + error });
            });
          });
        }).catch(error => {
          this.setState({ area: "Error getting seg img: " + error });
        });

      }).catch(error => {
        this.setState({ area: "Json error: " + error });
      })

    }).catch(response => {
      this.setState({ area: response });
    })
    
    // window.open("http://127.0.0.1:5000/address/'goethestr 9, 40670 Meerbusch'");
    return false;
  }

  priceSubmittedHandler = async (event) => {
    event.preventDefault();
    // this.setState({ price_per_kwh: document.getElementById("kwh-price").value });
  }

  // <a
  //className="App-link"
  //href="https://reactjs.org"
  //target="_blank"
  //rel="noopener noreferrer"
//>
  //Learn React
  //</a>

  //<img src={logo} className="App-logo" alt="logo" />

  render() {
    return (
      <div className="App">

        <h1 className="App-img">
        <img src={smileySun3} className="App-logo" alt="smileySun3" />
        </h1>

        <header className="App-header">
          <p>
            Calculate your Solar Potential!
          </p>
      
          <form>
            <label>
              Your Address:
              <input type="text" id="address-field" name="address-field" />
            </label>
            <input type="button" value="Submit" onClick={this.inputSubmittedHandler} />
          </form>

          <form>
            <label>
              Your current price per kWh:
              <input type="number" id="kwh-price" name="kwh-price" value="31.94" />
            </label>
          </form>

          <div className="App-container">
          <div className="App-product">
          <img src={placeholder_segmentation} alt="Available area for solar panels" id="seg-img" />
          <img src={placeholder_segmentation}  alt="Regular cost vs Solar" id="graph-img" />
          </div>
          </div>
          

          <div className="App-container">
          
          <h3 className = "App-info">

          <p>{this.state.area}</p>
          <p>{this.state.kwh_per_year}</p>
          <p>{this.state.mwh_per_life}</p>
          <p>{this.state.co2_per_year}</p>
          <p>{this.state.co2_per_life}</p>
          </h3>

          

          <h3 className = "App-info">
          <p>{this.state.area}</p>
          <p>{this.state.kwh_per_year}</p>
          <p>{this.state.mwh_per_life}</p>
          <p>{this.state.co2_per_year}</p>
          <p>{this.state.co2_per_life}</p>
          </h3>
          
          </div>

        </header>
      </div>
    );
  }
}

export default App;
