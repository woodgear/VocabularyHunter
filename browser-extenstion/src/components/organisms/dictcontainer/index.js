import React, { Component } from 'react'
import PropTypes from 'prop-types'
import './index.css'
import Sound from '../sound'

export default class DictContainer extends Component {
  static propTypes = {
    explains: PropTypes.arrayOf(PropTypes.object),
    currentIndex: PropTypes.number,
    actions: PropTypes.object
  };

  static defaultProps = {
    explains: [],
    currentIndex: 0
  };

  constructor (props) {
    super(props)
    this.state = { currentIndex: this.props.currentIndex }
    this.onClickNext = this.onClickNext.bind(this)
    this.onClickPre = this.onClickPre.bind(this)
    this.markKnow = this.markKnow.bind(this)
    this.markUnKnow = this.markUnKnow.bind(this)
  }

  onClickPre () {
    const commingIndex =
      (this.state.currentIndex - 1 + this.props.explains.length) %
      this.props.explains.length
    this.setState({
      currentIndex: commingIndex
    })
  }

  onClickNext () {
    const commingIndex =
      (this.state.currentIndex + 1 + this.props.explains.length) %
      this.props.explains.length
    this.setState({
      currentIndex: commingIndex
    })
  }

  getCurrentWordName () {
    if (this.state.currentIndex <= this.props.explains.length) {
      return this.props.explains[this.state.currentIndex].explain.name
    }
    return null
  }

  async markKnow () {
    const word = this.getCurrentWordName()
    if (word) {
      this.props.actions.markKnow(word)
      this.onClickNext()
    }
  }

  async markUnKnow () {
    const word = this.getCurrentWordName()
    if (word) {
      await this.props.actions.markUnKnow(word)
      this.onClickNext()
    }
  }

  renderWordExchange (exchange) {
    if (exchange) {
      return (
        <div className="word-exchange">
          {Object.entries(exchange).map(([exchageType, word]) => {
            return (
              <span key={exchageType}>
                {exchageType}:{word}
              </span>
            )
          })}
        </div>
      )
    } else {

    }
  }

  renderSound (word) {
    return (<div className="sound">
      <Sound word={word}/>
    </div>)
  }

  renderWordHead (name, phonetic, knowType) {
    console.log(name, phonetic, knowType)
    const knowTypeEle = (knowType => {
      if (knowType === 'know') {
        return <span className="word-knowtype know">k</span>
      }
      if (knowType === 'unknow') {
        return <span className="word-knowtype unknow">uk</span>
      }
    })(knowType)
    return (
      <div className="word-header">
        <span className="word-name">{name}</span>
        <div className="word-phonetic">
          <span>[{phonetic}]</span>
        </div>
        {this.renderSound(name)}
        <div className="knowtype"><span>{knowTypeEle}</span></div>
        <div className="word-index">
          <span>{this.state.currentIndex + 1}/{this.props.explains.length}</span>
        </div>
      </div>
    )
  }

  renderExplain (explain) {
    return (
      <div className="word-explain">
        <div className="word-explain-zh">
          {explain.translations.map((e, i) => (
            <p className="word-explain-item" key={i}>
              {e}
            </p>
          ))}
        </div>
        <div className="word-explain-en">
          {explain.definitions.map((e, i) => (
            <p className="word-explain-item" key={i}>
              {e}
            </p>
          ))}
        </div>
      </div>
    )
  }

  render () {
    if (this.props.explains.length === 0) {
      return (
        <div className="dict-container empty">
          <p>暂无数据</p>
        </div>
      )
    }

    const currentWord = this.props.explains[this.state.currentIndex]
    return (

      <div className={this.props.explains.length === 0 ? 'dict-container empty' : 'dict-container has-data'}>
        <div className="word-explain-container">
          {this.renderWordHead(
            currentWord.explain.name,
            currentWord.explain.phonetic,
            currentWord.know_type
          )}
          {this.renderWordExchange(currentWord.explain.exchange)}
          {this.renderExplain(currentWord.explain)}
        </div>
        <div className="vh-actions">
          <button className="vh-action-pre-uk" onClick={this.onClickPre}>
            {'<<'}
          </button>
          <button className="vh-action-mark-k" onClick={this.markKnow}>
            {'know'}
          </button>
          <button className="vh-action-mark-uk" onClick={this.markUnKnow}>
            {'unknow'}
          </button>

          <button className="vh-action-next-uk" onClick={this.onClickNext}>
            {'>>'}
          </button>
        </div>
      </div>
    )
  }
}
