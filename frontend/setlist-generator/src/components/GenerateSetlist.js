import React, { Component } from "react";
import { withRouter } from "react-router-dom";

const initialState = {
  numSongs: 0,
  numSlowSongs: 0,
  numEncores: 0,
  setOneOpener: "",
  setTwoOpener: "",
};

class GenerateSetlist extends Component {
  state = {
    ...initialState,
  };

  onChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  onSubmit = async (event) => {
    event.preventDefault();
    const queryString = `numSongs=${this.state.numSongs}&numSlowSongs=${this.state.numSlowSongs}&numEncores=${this.state.numEncores}&setOneOpener=${this.state.setOneOpener}&setTwoOpener=${this.state.setTwoOpener}`;
    //this.props.history.push(`/songlist?${queryString}`);
    const response = await fetch(
      `http://localhost:8000/generator/generate_setlist?${queryString}`
    );
    const data = await response.json();
    console.log(data);
    this.props.onSetlistGenerated(data);
    //this.setState(initialState);
  };

  render() {
    return (
      <form
        onSubmit={this.onSubmit}
        style={{
          textAlign: "center",
        }}
      >
        <label>
          No. of Songs
          <input
            type="number"
            name="numSongs"
            placeholder="0"
            value={this.state.numSongs}
            onChange={this.onChange}
            min="0"
            max="30"
          />
        </label>
        <label>
          No. of Slow Songs
          <input
            type="number"
            name="numSlowSongs"
            placeholder="0"
            value={this.state.numSlowSongs}
            onChange={this.onChange}
            min="0"
            max="30"
          />
        </label>
        <label>
          No. of Encores
          <input
            type="number"
            name="numEncores"
            placeholder="0"
            value={this.state.numEncores}
            onChange={this.onChange}
            min="0"
            max="30"
          />
        </label>
        <label>
          Set 1 Opener
          <input
            type="text"
            name="setOneOpener"
            value={this.state.setOneOpener}
            onChange={this.onChange}
          />
        </label>
        <label>
          Set 2 Opener
          <input
            type="text"
            name="setTwoOpener"
            value={this.state.setTwoOpener}
            onChange={this.onChange}
          />
        </label>
        <input type="submit" value="Generate Setlist" className="btn" />
      </form>
    );
  }
}
export default withRouter(GenerateSetlist);
