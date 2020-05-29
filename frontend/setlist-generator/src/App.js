import React, { Component } from "react";
import "./App.css";
import Songs from "./components/SongList.js";
import AddSong from "./components/AddSong.js";
import Header from "./components/layout/Header.js";
//rce-tab generates component
class App extends Component {
  state = {
    songs: [
      {
        id: 1,
        title: "Song1",
        artist: "example artist",
        isSlow: true,
        isWeaker: false,
      },
      {
        id: 2,
        title: "Song2",
        artist: "example artist2",
        isSlow: false,
        isWeaker: true,
      },
    ],
  };

  //toggle isWeaker  DOESNT WORK
  makeStronger = (id) => {
    this.setState({
      songs: this.state.songs.map((song) => {
        if (song.id === id) {
          song.isWeaker = !song.isWeaker;
        }
        return song;
      }),
    });
  };

  addSong = (title, isWeaker) => {
    const newSong = {
      title,
      isWeaker,
    };
    console.log({ newSong });

    this.setState({
      songs: [...this.state.songs, newSong],
    });
  };

  render() {
    return (
      <div className="App">
        <Header />
        <AddSong addSong={this.addSong} />
        <Songs songs={this.state.songs} makeStronger={this.makeStronger} />
      </div>
    );
  }
}
export default App;
