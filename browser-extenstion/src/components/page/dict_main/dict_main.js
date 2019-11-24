import './dict_main.css'
import React, { Component } from 'react'
import DictContainer from '../../organisms/dictcontainer'
import Api from '../../../api'
import * as bt from '../../../browser/browser_tool'
import PropTypes from 'prop-types'

class DcitMain extends Component {
  static propTypes = {
    userId: PropTypes.string,
    vhServer: PropTypes.string
  };

  constructor(props) {
    super(props)
    this.api = new Api(this.props.userId, this.props.vhServer)
    this.state = {
      article: '',
      explains: [],
      word: "",
      article: ""
    }
    this.actions = {
      markKnow: async word => {
        await this.api.markAsKnow([word])
        console.log('markKnow', word)
      },
      markUnKnow: async word => {
        await this.api.markAsUnKnow([word])
      }
    }
  }

  componentDidMount() {
    this.api.getExplain(["Durability"]).then(explains => {
      this.setState({ explains: explains })
    })


  }

  renderInput() {
    return (<div id="input-view">
      <div id="single-word">
        <span>查询单个单词:</span>
        <input id="word-input" onInput={(event) => {
          this.setState({ word: event.target.value })
        }
        } />
      </div>
      <div id="article">
        <span>查询文章:</span>
        <textarea id="article-input" onInput={(event) => {
          this.setState({ article: event.target.value })
        }
        } />

      </div>
      <div>
        <button id="search" onClick={async () => {
          let explain = []
          if (this.state.article !== "") {
            const words = await this.api.hunter(this.state.article);
            explain = await this.api.getExplain(words)
          } else {
            explain = await this.api.getExplain([this.state.word])
          }
          this.setState({ explains: explain })

        }}>查询</button>
      </div>

    </div>)
  }
  render() {
    return (
      <div className="App">
        {this.renderInput()}
        <DictContainer explains={this.state.explains} actions={this.actions} />
      </div>
    )
  }
}

export default DcitMain
