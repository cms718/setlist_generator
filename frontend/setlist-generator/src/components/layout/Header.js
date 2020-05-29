import React from "react";

export default function Header() {
  return (
    <header style={headerStyle}>
      <h1>Add Songs</h1>
    </header>
  );
}

const headerStyle = {
  background: "white",
  color: "black",
  textAlign: "center",
  padding: "10px",
};
