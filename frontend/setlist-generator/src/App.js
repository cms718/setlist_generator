import React, { Component } from "react";
import "./App.css";
import GenerateSetlist from "./components/GenerateSetlist.js";
import Header from "./components/layout/Header.js";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Setlist from "./components/Setlist";
//rcc-tab generates component
class App extends Component {
  state = {};

  render() {
    return (
      <Router>
        <div className="App">
          <Header />
          <GenerateSetlist
            onSetlistGenerated={(data) => {
              this.setState(data);
            }}
          />
          {this.state.band && (
            <Setlist
              setlistOne={this.state.setlist_one}
              setlistTwo={this.state.setlist_two}
            />
          )}
        </div>
      </Router>
    );
  }
}
export default App;
