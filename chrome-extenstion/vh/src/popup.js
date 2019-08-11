import "./popup.css";
import React, { Component } from "react";
import DictContainer from "./components/dictcontainer";
import Api from "./api";
import bt from "./broswer/tools";
const ID = "mock-id";

class PopUp extends Component {
  constructor(props) {
    super(props);
    this.api = new Api();
    this.state = { article: "", explains: [] };
    this.actions = {
      markKnow: async word => {
        await this.api.markAsKnow(ID, [word]);
        console.log("markKnow", word);
      },
      markUnKnow: async word => {
        await this.api.markAsUnKnow(ID, [word]);
      }
    };
  }
  componentDidMount() {
    bt.sendToContentScript({ action: "parser" }).then(async ({ article }) => {
      if (!!article) {
        console.log(article);
        const words = await this.api.hunter(ID, article);
        const explains = await this.api.getExplain(ID, words);
        console.log(explains)
        this.setState({ explains });
      } else {
        console.log("??? why undefine ???");
      }
    });
  }
  render() {
    return (
      <div className="App">
        <DictContainer explains={this.state.explains} actions={this.actions} />
      </div>
    );
  }
}

export default PopUp;
