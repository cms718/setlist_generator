import React, { Component } from "react";
import SongItem from "./SongItem";
import PropTypes from "prop-types";

class Songs extends Component {
  render() {
    return this.props.songs.map((song) => (
      <SongItem
        key={song.id}
        song={song}
        makeStronger={this.props.makeStronger}
        deleteSong={this.props.deleteSong}
      />
    ));
  }
}

// PropTypes
Songs.propTypes = {
  songs: PropTypes.array.isRequired,
};

export default Songs;
