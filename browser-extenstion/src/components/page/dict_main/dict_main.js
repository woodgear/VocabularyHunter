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
      words: [],
      article: "",
      current_explain_index:0
    }

    this.actions = {
      markKnow: async word => {
        await this.api.markAsKnow([word])
        console.log('markKnow', word)
      },
      markUnKnow: async word => {
        await this.api.markAsUnKnow([word])
      },
      getMoreExplain: async (step) => {
        const words = this.state.words;
        const current_explain_index = this.state.current_explain_index;
        const end_index = current_explain_index + step < words.length ? current_explain_index + step : words.length;
        const explains = await this.api.getExplain(words.slice(current_explain_index, end_index));
        const filledExplains = this.state.explains.concat(explains);
        this.setState({ explains: filledExplains, current_explain_index: end_index })
      }

    }
  }

  componentDidMount() {
  }

  renderInput() {
    return (<div id="input-view">
      <div id="single-word">
        <span>查询单个单词:</span>
        <input id="word-input" onInput={(event) => {
          this.setState({ words: [event.target.value] })
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
          if (this.state.article !== "") {
            const words = await this.api.hunter(this.state.article);
            this.setState({ words })
          }
          this.actions.getMoreExplain(10);
        }}>查询</button>
      </div>

    </div>)
  }
  render() {
    return (
      <div className="App">
        {this.renderInput()}
        <DictContainer explains={this.state.explains}
          totalExplainsLength={this.state.words.length}
          actions={this.actions} />
      </div>
    )
  }
}

export default DcitMain
