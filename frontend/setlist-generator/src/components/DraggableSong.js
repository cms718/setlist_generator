import React, { Component } from "react";
import styled from "styled-components";
import { Draggable } from "react-beautiful-dnd";
const Container = styled.div`
  border: 1px solid lightgrey;
  border-radius: 2px;
  padding: 8px;
  margin-bottom: 8px;
  background-color: white;
`;

class OuterContainer extends React.Component {
  render() {
    return (
      <Container {...this.props} ref={this.props.innerRef}>
        {this.props.children}
      </Container>
    );
  }
}

export default class DraggableSong extends Component {
  render() {
    return (
      <Draggable draggableId={`${this.props.song.id}`} index={this.props.index}>
        {(provided) => (
          <OuterContainer
            {...provided.draggableProps}
            {...provided.dragHandleProps}
            innerRef={provided.innerRef}
          >
            {this.props.song.title} - {this.props.song.song_key}
          </OuterContainer>
        )}
      </Draggable>
    );
  }
}
