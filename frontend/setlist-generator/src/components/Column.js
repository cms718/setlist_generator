import React, { Component } from "react";
import styled from "styled-components";
import DraggableSong from "./DraggableSong";
import { Droppable } from "react-beautiful-dnd";

const Container = styled.div`
  margin: 8px;
  border: 1px solid lightgrey;
  border-radius: 2px;
  width: 220px;
  display: flex;
  flex-direction: column;
`;
const Title = styled.h3`
  padding: 8px;
`;
const Setlist = styled.div`
  padding: 8px;
  flex-grow: 1;
  min-height: 100px;
`;

class SetlistContainer extends React.Component {
  render() {
    return (
      <Container {...this.props} ref={this.props.innerRef}>
        <Setlist>{this.props.children}</Setlist>
      </Container>
    );
  }
}

export default class Column extends Component {
  render() {
    return (
      <Container>
        <Title>{this.props.column.title}</Title>
        <Droppable droppableId={this.props.column.id}>
          {(provided) => (
            <SetlistContainer
              {...provided.droppableProps}
              innerRef={provided.innerRef}
            >
              {this.props.songs.map((song, index) => {
                return (
                  <DraggableSong key={song.id} song={song} index={index} />
                );
              })}
              {provided.placeholder}
            </SetlistContainer>
          )}
        </Droppable>
      </Container>
    );
  }
}
