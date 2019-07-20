import React, { Component } from "react";
import PropTypes from "prop-types";
import "./index.css";

export default class VocabularyHunterInput extends Component {
  static propTypes = {
    rawArticle: PropTypes.arrayOf(PropTypes.object),
  };

  constructor(props) {
    super(props);
    this.state = { rawArticle: this.props.rawArticle };
  }

  onClickParse() {
  }
  render() {
    return (
      <div className="vh-hunter-input">
      <textarea className="vh-hunter-input-text" ></textarea>
      <button onClick={this.onClickParse}>parse</button>
      </div>
      
    )
  }
}
