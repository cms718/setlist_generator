import React, { Component } from "react";

const initialState = {
  title: "",
  artist: "",
  isSlow: false,
  isWeaker: false,
  songKey: "",
};

export default class AddSong extends Component {
  state = {
    ...initialState,
  };

  onChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  onSubmit = (event) => {
    event.preventDefault();
    this.props.addSong(this.state.title, this.state.isWeaker);
    this.setState({ ...initialState });
  };

  render() {
    return (
      <form
        onSubmit={this.onSubmit}
        style={{
          textAlign: "center",
        }}
      >
        <input
          type="text"
          name="title"
          placeholder="Song Name"
          value={this.state.title}
          onChange={this.onChange}
        />
        <input
          type="text"
          name="artist"
          placeholder="Artist"
          value={this.state.artist}
          onChange={this.onChange}
        />
        <label>
          Is Slow?
          <input
            type="checkbox"
            name="isSlow"
            checked={this.state.isSlow}
            onClick={() => this.setState({ isSlow: !this.state.isSlow })}
          />
        </label>
        <label>
          Weaker Song?
          <input
            type="checkbox"
            name="isWeaker"
            checked={this.state.isWeaker}
            onClick={() => this.setState({ isWeaker: !this.state.isWeaker })}
          />
        </label>
        <label>
          Song Key
          <input
            type="text"
            name="songKey"
            value={this.state.songKey}
            onChange={this.onChange}
          />
        </label>
        <input type="submit" value="Submit" className="btn" />
      </form>
    );
  }
}
