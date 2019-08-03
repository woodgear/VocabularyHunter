import React, { Component } from "react";
import "./App.css";
import DictContainer from "./components/dictcontainer";
import VhInput from "./components/VHInput";
import Api from './api';

const ID = 'mock-id';

const defaultArticle = "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to Heaven, we were all going direct the other way—in short, the period was so far like the present period, that some of its noisiest authorities insisted on its being received, for good or for evil, in the superlative degree of comparison only."
class App extends Component {
  constructor(props) {
    super(props);
    this.onClickParse = this.onClickParse.bind(this);
    this.state = { article: '', explains: [] }
  }

  onClickParse(article) {
    console.log("app", article)
    const api = new Api();
    api.hunter(ID, article)
      .then((words) => {
        return api.getExplain(ID, words)
      })
      .then((explains) => {
        console.log("get explains", explains);
        this.setState({ explains })
      })
  }

  componentDidMount() {
    console.log("componentDidMount")
  }
  render() {
    console.log(this.state.explains)
    return (
      <div className="App">
        <VhInput rawArticle={defaultArticle} onClickParse={this.onClickParse} />
        <DictContainer explains={this.state.explains} />
      </div>
    );
  }
}

export default App;
