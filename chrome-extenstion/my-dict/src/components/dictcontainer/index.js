import React, { Component } from "react";
import PropTypes from "prop-types";
import "./index.css";

// const defaultProps =
export default class DictContainer extends Component {
  static propTypes = {
    explains: PropTypes.arrayOf(PropTypes.object),
    currentIndex: PropTypes.number
  };
  static defaultProps = {
    explains: [],
    currentIndex: 0
  };

  constructor(props) {
    super(props);
    this.state = { currentIndex: this.props.currentIndex };
    this.onClickNext = this.onClickNext.bind(this);
    this.onClickPre = this.onClickPre.bind(this);
  }

  onClickPre() {
    const commingIndex =
      (this.state.currentIndex - 1 + this.props.explains.length) %
      this.props.explains.length;
    this.setState({
      currentIndex: commingIndex
    });
  }

  onClickNext() {
    const commingIndex =
      (this.state.currentIndex + 1 + this.props.explains.length) %
      this.props.explains.length;
    this.setState({
      currentIndex: commingIndex
    });
  }

  renderWordExchange(exchange) {
    if (exchange) {
      return (
        <div className="word-exchange">
          {Object.entries(exchange).map(([e_type, word]) => {
            return (
              <span key={e_type}>
                {e_type}:{word}
              </span>
            );
          })}
        </div>
      );  
    }else {
      return 
    }
  }

  renderWordHead(name, phonetic, knowType) {
    // const audioUrl = `http://ssl.gstatic.com/dictionary/static/sounds/oxford/${name}--_gb_1.mp3`;
    const knowTypeEle = (knowType => {
      if (knowType === "know") {
        return <span className="word-knowtype know">k</span>;
      }
      if (knowType === "unknow") {
        return <span className="word-knowtype unknow">uk</span>;
      }
      return;
    })(knowType);
    return (
      <div className="word-header">
        <span className="word-name">{name}</span>
        <div className="word-phonetic">
          <span>{phonetic}</span>
        </div>
        {knowTypeEle}
      </div>
    );
  }

  renderExplain(explain) {
    return (
      <div className="word-explain">
        <div className="word-explain-zh">
          {explain.translations.map((e, i) => (
            <p key={i}>{e}</p>
          ))}
        </div>
        <div className="word-explain-en">
          {explain.definitions.map((e, i) => (
            <p key={i}>{e}</p>
          ))}
        </div>
      </div>
    );
  }

  render() {
    if (this.props.explains.length===0) {
      return (
        <div className="dict-container">
          <p>暂无数据</p>
        </div>
        )
    }

    const currentWord = this.props.explains[this.state.currentIndex];
    return (
      <div className="dict-container">
        <div className="word-explain-container">
          {this.renderWordHead(
            currentWord.explain.name,
            currentWord.explain.phonetic,
            currentWord["know_type"]
          )}
          {this.renderWordExchange(currentWord.explain.exchange)}
          {this.renderExplain(currentWord.explain)}
        </div>
        <div className="vh-actions">
          <button className="vh-action-pre-uk" onClick={this.onClickPre}>
            {"<<"}
          </button>
          <button className="vh-action-mark-k" onClick={this.markKnow}>
            {"know"}
          </button>
          <button className="vh-action-mark-uk" onClick={this.markUnKnow}>
            {"unknow"}
          </button>

          <button className="vh-action-next-uk" onClick={this.onClickNext}>
            {">>"}
          </button>
        </div>
      </div>
    );
  }
}
