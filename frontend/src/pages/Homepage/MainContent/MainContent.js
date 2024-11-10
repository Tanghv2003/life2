import React, { Component } from "react";
import Header from "../../../components/Header";
import Greeting from "./Greeting";
import Heart from "./Heart";

class MainContent extends Component {
  render() {
    return (
      <div className="main">
        <Header />
        <Greeting name = "Sophia"/>
        <Heart/>
      </div>
    );
  }
}

export default MainContent;
