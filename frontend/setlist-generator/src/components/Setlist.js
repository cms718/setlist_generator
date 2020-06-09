import React, { Component } from "react";

export default class Setlist extends Component {
  getStyle = () => {
    return {
      background: "white",
      padding: "8px",
      margin: "auto",
      width: "50%",
    };
  };

  render() {
    return (
      <div style={this.getStyle()}>
        <ul>
          {this.props.setlistOne.map(function (song, index) {
            return <li key={index}>{song.title}</li>;
          })}
        </ul>
        <ul>
          {this.props.setlistTwo.map(function (song, index) {
            return <li key={index}>{song.title}</li>;
          })}
        </ul>
      </div>
    );
  }
}
