import React, { Component } from "react";
import "./App.css";
import GenerateSetlist from "./components/GenerateSetlist.js";
import Header from "./components/layout/Header.js";
import { DragDropContext } from "react-beautiful-dnd";
import Column from "./components/Column";
import styled from "styled-components";

const Container = styled.div`
  display: flex;
`;

//TODO add empty column for reserve songs
//style containers
//add save button
//add band-name param for GenerateSetlist
//clean the backend with unused views etc.
class App extends Component {
  state = {
    columns: {
      "column-1": {
        id: "column-1",
        title: "Setlist 1",
        songIds: [],
      },
      "column-2": {
        id: "column-2",
        title: "Setlist 2",
        songIds: [],
      },
      "column-3": {
        id: "column-3",
        title: "Other Songs",
        songIds: [],
      },
    },
    columnOrder: ["column-1", "column-2", "column-3"],
  };

  onDragEnd = (result) => {
    const { destination, source, draggableId } = result;

    const intDraggableId = parseInt(draggableId);

    if (!destination) {
      return;
    }
    if (
      destination.droppableId === source.droppableId &&
      destination.index === source.index
    ) {
      return;
    }

    const start = this.state.columns[source.droppableId];
    const finish = this.state.columns[destination.droppableId];

    //moving in the same column
    if (start === finish) {
      const newSongIds = Array.from(start.songIds);
      newSongIds.splice(source.index, 1);
      newSongIds.splice(destination.index, 0, intDraggableId);

      const newColumn = {
        ...start,
        songIds: newSongIds,
      };

      const newState = {
        ...this.state,
        columns: {
          ...this.state.columns,
          [newColumn.id]: newColumn,
        },
      };

      this.setState(newState);
      return;
    }

    //moving between columns
    const startSongIds = Array.from(start.songIds);
    startSongIds.splice(source.index, 1);

    const newStart = {
      ...start,
      songIds: startSongIds,
    };

    const finishSongIds = Array.from(finish.songIds);
    finishSongIds.splice(destination.index, 0, intDraggableId);

    const newFinish = {
      ...finish,
      songIds: finishSongIds,
    };

    const newState = {
      ...this.state,
      columns: {
        ...this.state.columns,
        [newStart.id]: newStart,
        [newFinish.id]: newFinish,
      },
    };

    this.setState(newState);
  };

  render() {
    return (
      <div className="App">
        <Header />
        <GenerateSetlist
          onSetlistGenerated={(data) => {
            const columns = {
              "column-1": {
                ...this.state.columns["column-1"],
                songIds: data.setlist_one.map((song) => song.id),
                songs: data.setlist_one,
              },
              "column-2": {
                ...this.state.columns["column-2"],
                songIds: data.setlist_two.map((song) => song.id),
                songs: data.setlist_two,
              },
              "column-3": {
                ...this.state.columns["column-3"],
                songIds: data.reserve_songs.map((song) => song.id),
                songs: data.reserve_songs,
              },
            };

            this.setState({
              ...data,
              columns,
              songs: [
                ...data.setlist_one,
                ...data.setlist_two,
                ...data.reserve_songs,
              ],
            });
          }}
        />
        <Container>
          <DragDropContext
            onDragEnd={this.onDragEnd}
            onDragStart={this.onDragStart}
            onDragUpdate={this.onDragUpdate}
          >
            {this.state.band &&
              this.state.columnOrder.map((columnId) => {
                const column = this.state.columns[columnId];
                const songs = column.songIds.map((songId) => {
                  return this.state.songs.find((song) => song.id === songId);
                });
                return <Column key={column.id} column={column} songs={songs} />;
              })}
          </DragDropContext>
        </Container>
      </div>
    );
  }
}
export default App;
