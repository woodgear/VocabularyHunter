import React, { Component } from "react";
import PropTypes from "prop-types";
import "./index.css";

export default class VocabularyHunterInput extends Component {
  static propTypes = {
    rawArticle: PropTypes.string,
    //TODO
  };

  constructor(props) {
    super(props);
    this.state = { rawArticle: this.props.rawArticle };
    this.onTextChange = this.onTextChange.bind(this);
    this.onClickParse = this.onClickParse.bind(this);
    
  }
  onTextChange(event) {
    this.setState({rawArticle:event.target.value})
  }

  onClickParse() {
    this.props.onClickParse(this.state.rawArticle);
  }
  render() {
    return (
      <div className="vh-hunter-input">
      <textarea className="vh-hunter-input-text" defaultValue={this.state.rawArticle} onChange={this.onTextChange} ></textarea>
      <button onClick={this.onClickParse}>parse</button>
      </div>
      
    )
  }
}
