import React, { Component } from "react";
import PropTypes from "prop-types";

export class SongItem extends Component {
  getStyle = () => {
    return {
      background: "white",
      padding: "10px",
      borderBottom: "1px #ccc dotted",
      color: this.props.song.isWeaker ? "red" : "green",
    };
  };

  render() {
    return (
      <div style={this.getStyle()}>
        <p>
          <input
            type="checkbox"
            onChange={() => {
              this.props.makeStronger(this.props.song.id);
            }}
          />
          {this.props.song.title}
        </p>
      </div>
    );
  }
}
// PropTypes
SongItem.propTypes = {
  song: PropTypes.object.isRequired,
};

export default SongItem;
